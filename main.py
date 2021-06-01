"""
Run `sh update-schema.sh` to update houston schema
"""
import logging
import os

import yaml

import client
from client import env_vars
from client import houston_schema as schema
from client import users
from settings import CONFIG_PATH

logging.basicConfig(level=logging.DEBUG)


def main():
    config = load_config(CONFIG_PATH)
    config = client.apply_defaults(config)

    deployments = config["deployments"]

    for deployment_cfg in deployments:

        deployment = client.run(
            lambda q: q.deployment(
                where=schema.DeploymentWhereUniqueInput(
                    release_name=deployment_cfg["releaseName"]
                )
            )
        ).deployment

        env_vars.apply(deployment, deployment_cfg)
        users.apply(deployment, deployment_cfg)


def load_config(config_file) -> dict:
    if os.path.exists(config_file) is False:
        raise SystemExit("Config File not found! Exiting!")

    logging.info("Parsing config.yaml...")
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    return config


if __name__ == "__main__":
    main()
