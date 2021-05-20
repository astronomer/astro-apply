import logging

from client import compare
from client import houston_schema as schema
from client import run


def apply(deployment, deployment_cfg):

    logging.info(
        f"Applying Deployment Environment Variables for {deployment.release_name}..."
    )

    current_vars = parse_current(deployment)
    new_vars = parse_new(deployment_cfg)

    vars_to_add, vars_to_update, vars_to_delete = compare(current_vars, new_vars)

    # env vars don't have an add or delete function in houston
    # instead, we will need to pass all values if changes are needed
    vars_to_add.update(vars_to_update)
    logging.debug(f"Adding: {vars_to_add}\n Removing: {vars_to_delete} ")

    if vars_to_add or vars_to_delete:
        update(deployment, vars_to_add)

    else:
        logging.info(
            f"No Deployment Environment Variables need to be updated. Skipping..."
        )


def parse_current(deployment):
    return {
        env_var.key: env_var.__json_data__
        for env_var in deployment.environment_variables
    }


def parse_new(deployment_cfg):
    return {
        env_var["key"]: env_var
        for env_var in deployment_cfg.get("environmentVariables", [])
    }


def update(deployment, environment_variables):

    deployment_variables = {
        "deployment_uuid": deployment.id,
        "release_name": deployment.release_name,
        "environment_variables": [
            schema.InputEnvironmentVariable(
                key=value["key"], value=value["value"], is_secret=value["isSecret"]
            )
            for value in environment_variables.values()
        ],
    }

    run(
        lambda m: m.update_deployment_variables(**deployment_variables),
        is_mutation=True,
    )
