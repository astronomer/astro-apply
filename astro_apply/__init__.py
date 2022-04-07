from typing import Dict

import os

import click
import yaml
from click.exceptions import Exit
from dotenv import dotenv_values


def confirm_or_exit(msg: str, yes: bool = False) -> None:
    if not (yes or click.confirm(msg)):
        click.echo("Exiting...")
        raise Exit(1)


def houston_basedomain_to_api(source_basedomain: str) -> str:
    return f"https://houston.{source_basedomain}/v1"


def fetch_from_env(key):
    env = {**dotenv_values(".env"), **os.environ}
    return env.get(key)


def get_config_from_users_and_roles(
    workspace_id: str, users_and_roles: Dict[str, str]
) -> Dict[str, Dict[str, Dict[str, str]]]:
    r"""Creates config.yaml structure from a dump of username to workspace roles, for a given workspace
    :param workspace_id:
    :param users_and_roles:
    :return:
    >>> yaml.dump(get_config_from_users_and_roles(workspace_id="workspace_abcd1234", users_and_roles={"username_a": "WORKSPACE_ADMIN", "username_b": "WORKSPACE_EDITOR", "username_c": "WORKSPACE_VIEWER"}))
    'workspace_abcd1234:\n  users:\n    username_a: WORKSPACE_ADMIN\n    username_b: WORKSPACE_EDITOR\n    username_c: WORKSPACE_VIEWER\n'
    """
    return {workspace_id: {"users": users_and_roles}}
