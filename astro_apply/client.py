from typing import Any, Dict, List, Set, Tuple

import logging
from json import JSONDecodeError
from pathlib import Path
from urllib.parse import urlencode

import click
import requests
import yaml
from click.exceptions import Exit
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from requests.auth import AuthBase

from astro_apply.constants import (
    ASTRO_CLOUD_API_URL,
    ASTRO_CLOUD_AUTH_CLIENT_ID,
    ASTRO_CLOUD_AUTH_DOMAIN,
    ASTRO_CLOUD_ORGANIZATIONS,
    ASTRO_CLOUD_PRIVATE_ADD_WORKSPACE_USER_WITH_ROLE,
    ASTRO_CLOUD_PRIVATE_API_URL,
    ASTRO_CLOUD_PRIVATE_DELETE_WORKSPACE_USER,
    ASTRO_CLOUD_PRIVATE_UPDATE_WORKSPACE_USER_ROLE,
    ASTRO_CLOUD_PRIVATE_WORKSPACE_USERS_AND_ROLES,
    ASTRO_CLOUD_SELF,
    ASTRO_CLOUD_WORKSPACE_USERS_AND_IDS,
    ASTRO_CLOUD_WORKSPACES,
    HOUSTON_WORKSPACE_USERS_AND_ROLES,
    HOUSTON_WORKSPACES,
    SOFTWARE_TO_CLOUD_ROLE_MAPPINGS,
)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = f"Bearer {self.token}"
        return r


def extract_users_to_rolebindings(results, workspace_id_filter: str) -> Dict[str, List[Dict[str, str]]]:
    """extract_users_to_rolebindings -
    Flatten everything a bit
    mapping username -> [{.role, .workspace.id, .deployment.id, .deployment.label}, ...]
    all of the last three might be empty

    :param results: graphql query results set
    :param workspace_id_filter: workspace id to filter to
    :return: Dict[str, List[Dict[str, str]]] = {"<username>": [{ ... }, ...]}
    """
    users_to_rolebindings = {}
    for user in results["workspaceUsers"]:
        user_flat_roles = []
        for role in user["roleBindings"]:
            workspace_id = (role.get("workspace", {}) or {}).get("id")
            if (workspace_id == workspace_id_filter) or role.get("workspace") is None:
                user_flat_roles.append(
                    {
                        "role": role["role"],
                        "workspace_id": (role.get("workspace", {}) or {}).get("id"),
                        "deployment_id": (role.get("deployment", {}) or {}).get("id"),
                        "deployment_label": (role.get("deployment", {}) or {}).get("label"),
                    }
                )
        users_to_rolebindings[user["username"]] = user_flat_roles

    return users_to_rolebindings


def user_to_highest_rolebinding(users_to_rolebindings: Dict[str, List[Dict[str, str]]]) -> Dict[str, str]:
    """user_to_highest_rolebinding -
    Extract / Flatten graphql query - mapping a user to their highest rolebinding within a namespace
    (note: Astro Cloud doesn't have deployment RBAC, hence the mapping)
    :param users_to_rolebindings: graphql query results set
    :return: Dict[str, str] - {"<username>": "<highest role in workspace>", ...}

    """
    user_to_highest_role = {}
    for user, rolebindings in users_to_rolebindings.items():
        roles_only = [role["role"] for role in rolebindings]
        for role, mappings in SOFTWARE_TO_CLOUD_ROLE_MAPPINGS.items():
            if any(_role in roles_only for _role in mappings):
                user_to_highest_role[user] = role
                break

        if not user_to_highest_role.get(user):
            raise RuntimeError(f"We didn't map {user} with roles {roles_only} to any mapping")
    return user_to_highest_role


def filter_and_return_user_id_from_username(results: Any, username: str) -> str:
    """filter out the id for the username for ASTRO_CLOUD_WORKSPACE_USERS_AND_IDS
    (is there a direct username -> id lookup? I couldn't find one)
    :param results: GraphQL Result / Dict
    :param username: str
    :return: user id: str
    >>> test_results = {"workspaceUsers": [{"id": "right", "username": "foo@bar.com"}, {"id": "wrong", "username": "foo@baz.com"}]}
    >>> filter_and_return_user_id_from_username(test_results, "foo@bar.com")
    'right'
    >>> test_results = {"workspaceUsers": [{"id": "also_wrong", "username": "foo@bud.com"}, {"id": "wrong", "username": "foo@baz.com"}]}
    >>> filter_and_return_user_id_from_username(test_results, "foo@bar.com")
    Traceback (most recent call last):
    ...
    RuntimeError: unable to find id for user foo@bar.com in ASTRO_CLOUD_WORKSPACE_USERS_AND_IDS query - {'workspaceUsers': [{'id': 'also_wrong', 'username': 'foo@bud.com'}, {'id': 'wrong', 'username': 'foo@baz.com'}]}
    """
    user = [_user["id"] for _user in results.get("workspaceUsers", []) if _user["username"] == username]

    if not len(user):
        raise RuntimeError(
            f"unable to find id for user {username} in ASTRO_CLOUD_WORKSPACE_USERS_AND_IDS query - {results}"
        )
    else:
        return user[0]


def get_users_to_update_for_workspace(
    config_users_and_roles: Dict[str, str], existing_users_and_roles: Any
) -> Tuple[Dict[str, str], Dict[str, str], Set[str], Set[str]]:
    """
    :param config_users_and_roles:
    :param existing_users_and_roles:
    :return:
    """
    users_to_add = {
        user: config_users_and_roles[user] for user in set(config_users_and_roles).difference(existing_users_and_roles)
    }

    users_in_both = set(config_users_and_roles).intersection(existing_users_and_roles)
    users_to_delete = set(existing_users_and_roles).difference(config_users_and_roles)
    users_to_update = {
        user: role
        for user, role in config_users_and_roles.items()
        if user in existing_users_and_roles and existing_users_and_roles.get(user) != role
    }

    return users_to_update, users_to_add, users_to_delete, users_in_both


def _exec(client, query: str, variables: Dict[str, Any] = None):
    extra = {"variable_values": variables} if variables else {}
    log.debug(query, extra)
    return client.execute(gql(query), **extra)


class GQLClient:
    pass


class SoftwareClient(GQLClient):
    def __init__(self, url: str, workspace_sa_token: str = None):
        transport = RequestsHTTPTransport(
            url=url,
            auth=BearerAuth(workspace_sa_token),
            verify=True,
            retries=3,
        )
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def get_workspaces(self):
        return _exec(self.client, HOUSTON_WORKSPACES)

    def get_workspace_users_and_roles(self, workspace_id: str) -> Dict[str, str]:
        """
        Runs the constants.HOUSTON_WORKSPACE_USERS_AND_ROLES query,
        filters and extracts the highest role for a user in the given workspace,
        and maps roles via constants.SOFTWARE_TO_CLOUD_ROLE_MAPPINGS
        :param workspace_id:
        :return: Dict[str,str] - {"<username>": "<highest role mapping>", ...}
        """
        result = _exec(self.client, HOUSTON_WORKSPACE_USERS_AND_ROLES, {"workspaceUuid": workspace_id})
        users_to_rolebindings = extract_users_to_rolebindings(result, workspace_id)
        return user_to_highest_rolebinding(users_to_rolebindings)


def validate_workspace_role_or_raise(role: str, user: str, workspace_id: str) -> None:
    if role not in SOFTWARE_TO_CLOUD_ROLE_MAPPINGS:
        raise RuntimeError(
            f"unable to update user {user}, role {role}, in workspace {workspace_id} - role not in {SOFTWARE_TO_CLOUD_ROLE_MAPPINGS.keys()}"
        )


class CloudClient(GQLClient):
    def __init__(self):
        astrocloud_config_file = Path.home() / Path(".astrocloud/config.yaml")
        if not astrocloud_config_file.exists():
            click.echo("Unable to find initialized astrocloud config file. Please run `astrocloud auth login` first.")
            raise Exit(1)

        astrocloud_config = yaml.safe_load(astrocloud_config_file.open())

        if "contexts" not in astrocloud_config or "context" not in astrocloud_config:
            click.echo(
                "Unable to find 'context' and/or 'contexts' keys in astrocloud config file. "
                "Please run `astrocloud auth login` and/or report an error to solutions@astronomer.io."
            )
            raise Exit(1)

        current_context = astrocloud_config["contexts"][astrocloud_config["context"].replace(".", "_")]
        refresh_token = current_context.get("refreshtoken")

        has_error = False
        res = requests.post(
            f"{ASTRO_CLOUD_AUTH_DOMAIN}/oauth/token",
            data=urlencode(
                {"client_id": ASTRO_CLOUD_AUTH_CLIENT_ID, "grant_type": "refresh_token", "refresh_token": refresh_token}
            ),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if not res.ok:
            has_error = True
        else:
            try:
                if "access_token" not in res.json():
                    has_error = True
                else:
                    access_token = res.json()["access_token"]
                    self.client = Client(
                        transport=RequestsHTTPTransport(
                            url=ASTRO_CLOUD_API_URL, auth=BearerAuth(access_token), verify=True, retries=3
                        ),
                        fetch_schema_from_transport=False,
                    )
                    self.private_client = Client(
                        transport=RequestsHTTPTransport(
                            url=ASTRO_CLOUD_PRIVATE_API_URL, auth=BearerAuth(access_token), verify=True, retries=3
                        ),
                        fetch_schema_from_transport=False,
                    )
            except JSONDecodeError:
                has_error = True

        if has_error:
            click.echo("Token refresh failed - check your internet, or try running astrocloud auth login first")
            click.echo(f"{res.status_code} - {res.content}")
            raise Exit(1)

    def get_workspace_users_and_roles(self, workspace_id: str) -> Dict[str, str]:
        result = _exec(
            self.private_client, ASTRO_CLOUD_PRIVATE_WORKSPACE_USERS_AND_ROLES, variables={"workspaceId": workspace_id}
        )
        users_to_rolebindings = extract_users_to_rolebindings(result, workspace_id)
        return user_to_highest_rolebinding(users_to_rolebindings)

    def get_workspaces(self):
        """deprecated / unnecessary - we have workspaces in the config file"""
        for _, org_id in self.get_organizations().items():
            print(org_id, _exec(self.client, ASTRO_CLOUD_WORKSPACES, variables={"organizationId": org_id}))

    def get_organizations(self) -> Dict[str, str]:
        return {org["name"]: org["id"] for org in _exec(self.client, ASTRO_CLOUD_ORGANIZATIONS)["organizations"]}

    def get_self(self) -> Any:
        """deprecated / unnecessary"""
        return _exec(self.client, ASTRO_CLOUD_SELF)

    def add_workspace_user_with_role(self, user: str, role: str, workspace_id: str) -> Any:
        validate_workspace_role_or_raise(role, user, workspace_id)
        return _exec(
            self.private_client,
            ASTRO_CLOUD_PRIVATE_ADD_WORKSPACE_USER_WITH_ROLE,
            variables={"workspaceId": workspace_id, "email": user, "role": role, "deploymentRoles": []},
        )

    def update_workspace_user_with_role(self, user: str, role: str, workspace_id: str) -> Any:
        validate_workspace_role_or_raise(role, user, workspace_id)
        return _exec(
            self.private_client,
            ASTRO_CLOUD_PRIVATE_UPDATE_WORKSPACE_USER_ROLE,
            variables={"email": user, "role": role, "workspaceId": workspace_id},
        )

    def delete_workspace_user(self, user: str, workspace_id: str) -> Any:
        user_id = self.get_user_id_from_username(user, workspace_id)
        return _exec(
            self.private_client,
            ASTRO_CLOUD_PRIVATE_DELETE_WORKSPACE_USER,
            variables={"userId": user_id, "workspaceId": workspace_id},
        )

    def get_user_id_from_username(self, username: str, workspace_id: str) -> str:
        results = _exec(self.client, ASTRO_CLOUD_WORKSPACE_USERS_AND_IDS, variables={"workspaceUsersId": workspace_id})
        return filter_and_return_user_id_from_username(results, username)
