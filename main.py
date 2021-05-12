"""
Run `sh update-schema.sh` to update houston schema
"""
import logging

import client
from client import env_vars
from client import houston_schema as schema
from client import users

logging.basicConfig(level=logging.DEBUG)


def main():
    config = client.load_config()
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


if __name__ == "__main__":
    main()
