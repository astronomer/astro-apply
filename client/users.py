import logging

from client import run, compare


def apply(deployment, deployment_cfg):
    logging.info(
        f"Applying Users for {deployment.release_name} in {deployment.workspace.label}..."
    )

    def ws_users(q):
        q.workspace_users(workspace_uuid=deployment.workspace.id).username()
        q.workspace_users.role_bindings()
        q.workspace_users.role_bindings.role()
        q.workspace_users.role_bindings.workspace.__fields__("id", "label")
        q.workspace_users.role_bindings.deployment.__fields__("id", "label", "release_name")

    ws_users = run(ws_users).workspace_users

    current_user_roles = user_roles(ws_users, deployment)
    new_user_roles = {cfg_user["username"]: cfg_user for cfg_user in deployment_cfg["users"]}

    users_to_add, users_to_update, users_to_delete = compare(current_user_roles, new_user_roles)

    # TODO:
    #  1. If users_to_add --> invite user to workspace, add user to deployment
    #  2. If users_to_update --> update user role
    #  3. If users_to_delete --> remove user from deployment, leave in workspace in case they are part of a different deployment


def user_roles(ws_users, deployment):
    roles = {}
    for user in ws_users:
        workspace_roles = [
            rb.role for rb in user.role_bindings if rb.role.startswith("WORKSPACE") and rb.workspace.id == deployment.workspace.id
        ]
        deployment_roles = [
            rb.role for rb in user.role_bindings if rb.role.startswith("DEPLOYMENT") and rb.deployment.id == deployment.id
        ]
        roles[user.username] = {
            "username": user.username,
            "roles":
                {
                    "workspace": workspace_roles[0],
                    "deployment": deployment_roles[0]
                }
        }
    return roles
