import logging

from client import compare
from client import houston_schema as schema
from client import run


def apply(deployment, deployment_cfg):
    logging.info(
        f"Applying Users for {deployment.release_name} in {deployment.workspace.label}..."
    )

    def ws_users(q):
        q.workspace_users(workspace_uuid=deployment.workspace.id).__fields__(
            "id", "username"
        )
        q.workspace_users.role_bindings()
        q.workspace_users.role_bindings.role()
        q.workspace_users.role_bindings.workspace.__fields__("id", "label")
        q.workspace_users.role_bindings.deployment.__fields__(
            "id", "label", "release_name"
        )

    ws_users = run(ws_users).workspace_users

    current_user_roles = parse_current(ws_users, deployment)
    new_user_roles = parse_new(deployment_cfg)

    users_to_add, users_to_update, users_to_delete = compare(
        current_user_roles, new_user_roles
    )

    if not users_to_add and not users_to_update and not users_to_delete:
        logging.info("No Users need to be updated. Skipping... ")

    else:

        if users_to_add:
            for user in users_to_add.values():
                add_(deployment, user)

        if users_to_update:
            for user in users_to_update.values():
                user["user_id"] = filter_user_id(user, ws_users)
                update(deployment, user)

        if users_to_delete:
            for user in users_to_delete.values():
                user["user_id"] = filter_user_id(user, ws_users)
                delete(deployment, user)


def parse_current(ws_users, deployment):
    roles = {}
    for user in ws_users:

        roles[user.username] = {
            "username": user.username,
            "role": next(
                filter(
                    lambda r: r.role.startswith("DEPLOYMENT")
                    and r.deployment.id == deployment.id,
                    user.role_bindings,
                )
            ).role,
        }

    return roles


def parse_new(deployment_cfg):
    return {
        cfg_user["username"]: cfg_user for cfg_user in deployment_cfg.get("users", [])
    }


def filter_user_id(user, ws_users):
    return next(filter(lambda x: x["username"] == user["username"], ws_users)).id


def add_(deployment, user: dict):
    user = {
        "email": user["username"],
        "workspace_uuid": deployment.workspace.id,
        "deployment_roles": [
            schema.DeploymentRoles(deployment_id=deployment.id, role=user["role"])
        ],
    }
    logging.debug(f"Adding {user}")
    run(
        lambda m: m.workspace_add_user(**user),
        is_mutation=True,
    )


def update(deployment, user: dict):
    user = {
        "user_id": user["user_id"],
        "deployment_id": deployment.id,
        "email": user["username"],
        "role": user["role"],
    }
    logging.debug(f"Updating {user}")
    run(lambda m: m.deployment_update_user_role(**user), is_mutation=True)


def delete(deployment, user: dict):
    user = {
        "user_id": user["user_id"],
        "deployment_id": deployment.id,
        "email": user["username"],
    }
    logging.debug(f"Deleting {user}")
    run(lambda m: m.deployment_remove_user_role(**user), is_mutation=True)
