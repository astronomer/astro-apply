"""
Run `sh update-schema.sh` to update houston schema
"""
import yaml
import os
import logging
from typing import Dict, Tuple, Optional
import copy

from dotenv import dotenv_values

from deepdiff import DeepDiff
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

from houston_schema import houston_schema as schema

logging.basicConfig(level=logging.INFO)

REQUIRED_VARS = [
    "BASEURL",  # e.g.  astro.mydomain.com
    "TOKEN",  # either a service account token or a temporary one obtained from app.BASEURL/token
]

env = {**dotenv_values(".env"), **os.environ}
for var in REQUIRED_VARS:
    if var not in env:
        raise SystemExit(f"Required env var {var} not found! Exiting!")

URL = f'https://houston.{env["BASEURL"]}/v1'
HEADERS = {"Authorization": env["TOKEN"]}
CONFIG_FILE = env.get("ASTRO_CONFIG", "config.yaml")


def load_config() -> dict:
    if os.path.exists(CONFIG_FILE) is False:
        raise SystemExit("Config File not found! Exiting!")

    logging.info("Parsing config.yaml...")
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)

    return config


def run(fn, is_mutation: bool = False, **kwargs):
    """
    Run graphql query or mutation against Houston API.
    Returns response as ORM
    """
    endpoint = HTTPEndpoint(URL, HEADERS)
    query = Operation(schema.Mutation if is_mutation else schema.Query)
    fn(query, **kwargs)
    return query + endpoint(query)


def compare(
    actual_values: Optional[Dict[str, dict]], desired_values: Optional[Dict[str, dict]]
) -> Tuple[dict, dict]:
    """
    Compares current values with values from config against current configuration.
    Returns a dict of items to add, and a dict of items to delete so they can be passed to Houston
    """

    actual_values = actual_values or {}
    desired_values = desired_values or {}

    values_to_add = copy.deepcopy(desired_values)
    values_to_delete = copy.deepcopy(actual_values)

    for key in list(desired_values.keys()):
        if key in actual_values and not DeepDiff(
            actual_values[key], desired_values[key]
        ):
            values_to_add.pop(key)
            values_to_delete.pop(key)

    return values_to_add, values_to_delete


def update_environment_variables(deployment, environment_variables):
    deployment_variables = [
        schema.InputEnvironmentVariable(
            key=value["key"], value=value["value"], is_secret=value["isSecret"]
        )
        for value in environment_variables.values()
    ]
    update_deployment_variables_args = {
        "deployment_uuid": deployment.id,
        "release_name": deployment.release_name,
        "environment_variables": deployment_variables,
    }
    run(
        lambda m: m.update_deployment_variables(
            **update_deployment_variables_args
        ),
        is_mutation=True,
    )


def main():
    config = load_config()
    deployments = config["deployments"]

    for d in deployments:
        deployment = run(
            lambda q: q.deployment(
                where=schema.DeploymentWhereUniqueInput(
                    release_name=d["releaseName"]
                )
            )
        ).deployment

        logging.info(
            f"Applying Deployment Environment Variables for {deployment.release_name}..."
        )

        environment_variables = {
            env_var.key: env_var.__json_data__
            for env_var in deployment.environment_variables
        }
        new_environment_variables = {
            env_var["key"]: env_var
            for env_var in deployment.get("environmentVariables", [])
        }

        # env vars are one of the few things that don't have an add or delete function in houston
        # instead, we will need to pass all values everytime
        # to avoid unnecessary calls, we check if there are changes
        vars_to_add, vars_to_delete = compare(environment_variables, new_environment_variables)
        logging.debug(f"Adding: {vars_to_add}\n Removing: {vars_to_delete} ")

        # if yes, use values directly from config
        if vars_to_add or vars_to_delete:
            update_environment_variables(deployment, new_environment_variables)

        else:
            logging.info(
                f"No Deployment Environment Variables need to be updated. Skipping..."
            )


# def main():
#     logging.info("Parsing config.yaml...")
#     with open(CONFIG_FILE, 'r') as f:
#         config = yaml.safe_load(f)
#         workspaces = config['workspaces']
#         logging.info(f"Applying {len(workspaces)} workspaces...")
#
#         def _ws(q):
#             q.workspaces.__fields__(*WORKSPACE_FIELDS)
#             q.workspaces.deployments.__fields__(__exclude__=EXCLUDED_DEPLOYMENT_FIELDS)
#             q.workspaces.deployments.webserver.__fields__()
#         found_ws = {ws.label: ws for ws in run(_ws).workspaces}
#         for i, workspace in enumerate(workspaces):
#             if workspace['label'] in found_ws:
#                 logging.info(f"({i+1}/{len(workspaces)}) Workspace {workspace['label']} already found... skipping creation...")
#                 actual_workspace = found_ws[workspace['label']]
#             else:
#                 logging.warning("Workspaces must be created ahead of time due to service account limitations, unless running with a user token...")
#                 logging.info(f"({i+1}/{len(workspaces)}) Creating Workspace {workspace['label']}...")
#                 actual_workspace = run(lambda m: m.create_workspace(
#                     label=workspace['label'],
#                     description=workspace.get('description')
#                 ).__fields__('id', 'label'), is_mutation=True)
#                 # todo: AttributeError: 'Mutation' object has no attribute 'id'
#
#             logging.info(f"Applying {len(workspace['deployments'])} Deployments for {workspace['label']}...")
#             found_deployments = {dp.label: dp for dp in actual_workspace.deployments}
#             for j, deployment in enumerate(workspace['deployments']):
#                 if deployment['label'] in found_deployments:
#                     logging.info(f"({j+1}/{len(workspace['deployments'])}) Deployment {deployment['label']} already found... skipping creation...")
#                     # todo: update_deployment
#                 else:
#                     logging.info(f"({j+1}/{len(workspace['deployments'])}) Creating Deployment {deployment['label']}...")
#                     create_deployment_args = dict({
#                             'workspace_uuid': actual_workspace.id,
#                             'type': 'airflow',
#                             'label': deployment['label'],
#                             'executor': deployment['executor']
#                         },
#                         **{"release_name": deployment['releaseName']} if deployment['releaseName'] else {}
#                     )
#                     actual_deployment = run(lambda m: m.create_deployment(**create_deployment_args), is_mutation=True)
#                     # todo: update deployment (webserver/scheduler/workers)
#                     # todo: deployment_add_user_role
#
#                 logging.info(f"Applying Deployment Environment Variables...")
#                 # todo: update_deployment_variables
#
#             logging.info(f"Applying {len(workspace['users'])} Workspace Users for {workspace['label']}...")
#             for j, user in enumerate(workspace['users']):
#                 logging.info(f"({j+1}/{len(workspace['users'])}) Creating Workspace User {user['email']} with Role {user['role']}...")
#                 # todo: workspaceUpdateUserRole ?
#                 # todo: check if user is already there first?
#                 added_user = run(lambda m: m.workspace_add_user(
#                     email=user['email'],
#                     role=user['role'],
#                     workspace_uuid=actual_workspace.id,
#                     deployment_roles=user['deploymentRoles']
#                 ), is_mutation=True)


if __name__ == "__main__":
    main()
