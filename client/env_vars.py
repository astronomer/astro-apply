import logging

from client import houston_schema as schema, run, compare


def apply(deployment, deployment_cfg):
    logging.info(
        f"Applying Deployment Environment Variables for {deployment.release_name}..."
    )
    current_env_vars = {
        env_var.key: env_var.__json_data__
        for env_var in deployment.environment_variables
    }
    new_env_vars = {
        env_var["key"]: env_var
        for env_var in deployment_cfg.get("environmentVariables", [])
    }
    # env vars don't have an add or delete function in houston
    # instead, we will need to pass all values if changes are needed
    env_vars_to_add, env_vars_to_delete = compare(current_env_vars, new_env_vars)
    logging.debug(f"Adding: {env_vars_to_add}\n Removing: {env_vars_to_delete} ")
    # if yes, use values directly from config
    if env_vars_to_add or env_vars_to_delete:
        _update(deployment, new_env_vars)

    else:
        logging.info(
            f"No Deployment Environment Variables need to be updated. Skipping..."
        )


def _update(deployment, environment_variables):
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
