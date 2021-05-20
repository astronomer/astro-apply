import pytest

import client

foo = {"key": "FOO", "value": "foo", "is_secret": False}
bar = {"key": "FOO", "value": "bar", "is_secret": False}
baz = {"key": "BAZ", "value": "baz", "is_secret": False}
FOO = {"FOO": foo}
BAR = {"FOO": bar}
BAZ = {"BAZ": baz}
FOO_BAZ = {"FOO": foo, "BAZ": baz}

# (actual, desired, expected_to_add, expected_to_delete, expected_to_udate)
compare_test_data = [
    (FOO, FOO, {}, {}, {}),  # nothing changes, add:0 del:0 update:0
    (FOO, BAR, {}, {}, BAR),  # env var value changes, add:0 del:0 update:1
    (
        FOO_BAZ,
        FOO,
        {},
        BAZ,
        {},
    ),  # two env vars, remove 1 env var from config - add:0 del:1 update: 0
    (
        FOO,
        FOO_BAZ,
        BAZ,
        {},
        {},
    ),  # one env var exists, one to be added from config - add:1 del:0 update:0
    (
        None,
        FOO,
        FOO,
        {},
        {},
    ),  # no env vars exist, one to be added from config add:1 del:0 update:0
    (FOO, None, {}, FOO, {}),  # one env var exists, none listed in config add:0 del: 1 update:0
]


@pytest.mark.parametrize(
    "actual,desired,expected_to_add,expected_to_delete,expected_to_update",
    compare_test_data,
)
def test_compare(
    actual, desired, expected_to_add, expected_to_delete, expected_to_update
):
    to_add, to_update, to_delete = client.compare(actual, desired)
    assert to_add == expected_to_add
    assert to_delete == expected_to_delete
    assert to_update == expected_to_update


def test_run_query(monkeypatch):
    def mock_call(*args):
        return {"data": {"workspaceUsers": []}}

    from sgqlc.endpoint.http import HTTPEndpoint

    monkeypatch.setattr(HTTPEndpoint, "__call__", mock_call)
    query = client.run(lambda q: q.workspace_users(workspace_uuid="test_id"))
    assert type(query) == client.houston_schema.Query


def test_run_mutation(monkeypatch):
    def mock_call(*args):
        return {"data": {"workspaceAddUser": None}}

    from sgqlc.endpoint.http import HTTPEndpoint

    monkeypatch.setattr(HTTPEndpoint, "__call__", mock_call)

    kwargs = {
        "email": "some_email",
        "workspace_uuid": "some_workspace_id",
        "deployment_roles": [
            client.houston_schema.DeploymentRoles(
                deployment_id="some_deployment_id", role="DEPLOYMENT_ADMIN"
            )
        ],
    }

    mutation = client.run(
        lambda m: m.workspace_add_user(**kwargs),
        is_mutation=True,
    )
    assert type(mutation) == client.houston_schema.Mutation


# test user objects
some_user = {"username": "some_user@example.com", "role": "DEPLOYMENT_ADMIN"}
some_other_user = {"username": "some_other_user", "role": "DEPLOYMENT_VIEWER"}

# test environment variables
cluster_name = {"key": "CLUSTER_NAME", "value": "SOME_CLUSTER_NAME", "isSecret": False}
environment_name = {"key": "ENVIRONMENT", "value": "TEST", "isSecret": False}

# test deployments
some_deployment = {
    "releaseName": "some-release-name-5555",
    "workspace": "some-workspace",
}

# mock config
test_config_1 = {
    "users": [some_user],
    "environmentVariables": [cluster_name],
    "deployments": [
        {
            "releaseName": some_deployment["releaseName"],
            "workspace": some_deployment["workspace"],
            "users": [some_other_user],
            "environmentVariables": [environment_name]
         }
    ]
}

expected_config_1 = {
    "users": [some_user],
    "environmentVariables": [cluster_name],
    "deployments": [
        {
            "releaseName": some_deployment["releaseName"],
            "workspace": some_deployment["workspace"],
            "users": [some_other_user, some_user],
            "environmentVariables": [environment_name, cluster_name]
        }
    ]
}

# mock config
test_config_2 = {
    "users": [some_user],
    "environmentVariables": [cluster_name],
    "deployments": [
        {
            "releaseName": some_deployment["releaseName"],
            "workspace": some_deployment["workspace"],
         }
    ]
}

expected_config_2 = {
    "users": [some_user],
    "environmentVariables": [cluster_name],
    "deployments": [
        {
            "releaseName": some_deployment["releaseName"],
            "workspace": some_deployment["workspace"],
            "users": [some_user],
            "environmentVariables": [cluster_name]
        }
    ]
}

apply_test_data = [
    (test_config_1, expected_config_1),
    (test_config_2, expected_config_2)
]


@pytest.mark.parametrize(
    "test_config,expected_config",
    apply_test_data,
)
def test_apply_defaults(test_config, expected_config):
    modified_config = client.apply_defaults(test_config)
    from deepdiff import DeepDiff
    diff = DeepDiff(modified_config, expected_config)
    assert not diff
