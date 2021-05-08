"""
Run `sh update-schema.sh` to update houston schema
"""
import yaml
import os
import logging

import client
from client import houston_schema as schema, env_vars, CONFIG_FILE

logging.basicConfig(level=logging.INFO)


def main():
    config = load_config()
    deployments = config["deployments"]

    for d in deployments:
        deployment = client.run(
            lambda q: q.deployment(
                where=schema.DeploymentWhereUniqueInput(
                    release_name=d["releaseName"]
                )
            )
        ).deployment

        env_vars.apply(deployment)


def load_config() -> dict:
    if os.path.exists(CONFIG_FILE) is False:
        raise SystemExit("Config File not found! Exiting!")

    logging.info("Parsing config.yaml...")
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)

    return config


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
