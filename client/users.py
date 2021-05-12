import logging

from client import compare
from client import houston_schema as schema
from client import run


def apply(deployment, deployment_cfg):
    logging.info(
        f"Applying Users for {deployment.release_name} in {deployment.workspace.label}..."
    )

    def ws_users(q):
        q.workspace_users(workspace_uuid=deployment.workspace.id).username()
        q.workspace_users.role_bindings()
        q.workspace_users.role_bindings.role()
        q.workspace_users.role_bindings.workspace.__fields__("id", "label")
        q.workspace_users.role_bindings.deployment.__fields__(
            "id", "label", "release_name"
        )

    ws_users = run(ws_users).workspace_users

    current_user_roles = filter_roles(ws_users, deployment)
    new_user_roles = {
        cfg_user["username"]: cfg_user for cfg_user in deployment_cfg["users"]
    }

    users_to_add, users_to_update, users_to_delete = compare(
        current_user_roles, new_user_roles
    )

    if users_to_add:
        for user in users_to_add.values():

            workspace_add_user_args = {
                "email": user["username"],
                "workspace_uuid": deployment.workspace.id,
                "deployment_roles": [
                    schema.DeploymentRoles(
                        deployment_id=deployment.id, role=user["role"]
                    )
                ],
            }

            run(
                lambda m: m.workspace_add_user(**workspace_add_user_args),
                is_mutation=True,
            )

    # TODO:
    #  1. If users_to_update --> update user role
    #  2. If users_to_delete --> remove user from deployment, leave in workspace in case they are part of a different deployment


def filter_roles(ws_users, deployment):
    roles = {}
    for user in ws_users:

        def deploy_id(r, id_=deployment.id):
            return r.role.startswith("DEPLOYMENT") and r.deployment.id == id_

        roles[user.username] = {
            "username": user.username,
            "role": next(filter(deploy_id, user.role_bindings)).role,
        }

    return roles
