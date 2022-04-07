from typing import Set

from pathlib import Path

import click
import deepmerge
import yaml
from click import UsageError
from dotenv import load_dotenv
from gql.transport.exceptions import TransportQueryError

from astro_apply import confirm_or_exit, get_config_from_users_and_roles, houston_basedomain_to_api
from astro_apply.client import CloudClient, SoftwareClient
from astro_apply.constants import ASTRO_CLOUD_API_URL, ASTRO_CLOUD_BASEDOMAIN, NEBULA_BASEDOMAIN_URL

d = {"show_default": True, "show_envvar": True}
fd = {"show_default": True, "show_envvar": True, "is_flag": True}
rp = {"prompt": True, "required": True}


@click.group()
@click.version_option()
def cli():
    """astro-apply - like kubectl apply but for Astronomer Cloud"""
    pass


@cli.command()
@click.option(
    "--target-workspace-id",
    **rp,
    **d,
    help="Target Workspace ID - should look something like cku5ts93v10865546pinw23j7m7g",
)
@click.option(
    "--source-workspace-id",
    **rp,
    **d,
    help="Source Workspace ID - should look something like cku5ts93v10865546pinw23j7m7g",
)
@click.option(
    "--basedomain",
    "-d",
    default=NEBULA_BASEDOMAIN_URL,
    **d,
    help="e.g. example.com if you access astronomer via https://app.example.com. "
    "If empty - defaults to Nebula. "
    "Can be cloud.astronomer.io to fetch from Astronomer Cloud",
)
@click.option(
    "--output-file",
    "-f",
    prompt=True,
    default="config.yaml",
    **d,
    type=click.Path(dir_okay=False, writable=True),
    help="Output file to write to or merge with",
)
@click.option(
    "--workspace-service-account-token",
    "-t",
    **d,
    help="Workspace Service Account Token - input hidden when prompted for",
)
@click.option("--yes", "-y", is_flag=True, default=False, help="Skip confirmation prompts")
def fetch(
    target_workspace_id: str,
    source_workspace_id: str,
    basedomain: str,
    output_file: str,
    workspace_service_account_token: str,
    yes: bool,
):
    """Fetch existing configuration from an Astronomer workspace"""
    if basedomain in ASTRO_CLOUD_BASEDOMAIN:
        client = CloudClient()
        url = ASTRO_CLOUD_API_URL
    else:
        if workspace_service_account_token is None:
            workspace_service_account_token = click.prompt(
                text="Workspace Service Account Token:", hide_input=True, type=str
            )
        url = houston_basedomain_to_api(basedomain)
        client = SoftwareClient(url, workspace_service_account_token)

    confirm_or_exit(
        f"Querying {url} for Workspace '{source_workspace_id}' configurations, saving to {output_file} - Continue?", yes
    )

    try:
        users_and_roles = client.get_workspace_users_and_roles(source_workspace_id)
        users_and_roles_sample = ", ".join([f"{u}: {r}" for u, r in list(users_and_roles.items())[:3]])
    except TransportQueryError as e:
        raise UsageError(str(e)) from e

    confirm_or_exit(f"Found {len(users_and_roles)} users and roles - {users_and_roles_sample}, ... - Continue?", yes)

    partial_config = get_config_from_users_and_roles(target_workspace_id, users_and_roles)
    if Path(output_file).exists():
        click.echo(f"Found existing content at {output_file}, merging content for Workspace '{source_workspace_id}'...")
        with click.open_file(output_file, mode="r") as f:
            config = deepmerge.always_merger.merge(yaml.safe_load(f), partial_config)
    else:
        click.echo(f"Writing content for Workspace '{source_workspace_id}' to {output_file}...")
        config = partial_config

    with click.open_file(output_file, mode="w") as f:
        yaml.safe_dump(config, f)
    click.echo(f"Wrote to {output_file}!")


# def update_workspace(workspace_id: str, config_users_and_roles: Dict[str, str], client: CloudClient, input_file: str, yes: bool):


def delete_users(users_to_delete: Set[str], client: CloudClient, workspace_id: str):
    if len(users_to_delete) and click.confirm(
        f"Found {len(users_to_delete)} users in to delete: {users_to_delete} - Continue?"
    ):
        for user in users_to_delete:
            click.echo(f"Deleting user: {user}")
            client.delete_workspace_user(user, workspace_id)


@cli.command()
@click.option(
    "--input-file",
    "-f",
    prompt=True,
    default="config.yaml",
    **d,
    type=click.Path(dir_okay=False, readable=True, exists=True),
    help="Input configuration file to read - see README.md for a sample",
)
@click.option("--yes", "-y", is_flag=True, default=False, help="Skip confirmation prompts")
def apply(input_file: str, yes: bool):
    """Apply a configuration to an Astronomer Cloud workspaces"""

    with open(input_file) as f:
        config = yaml.safe_load(f)

    if not config or not len(config.keys()):
        raise UsageError(f"{input_file} is empty or an error occurred, exiting!")

    client = CloudClient()

    click.echo(f"Applying {input_file} and {len(config.keys())} workspace(s)...")

    for workspace_id, contents in config.items():
        config_users_and_roles = contents["users"]
        config_users_and_roles_sample = ", ".join([f"{u}: {r}" for u, r in list(config_users_and_roles.items())[:3]])

        confirm_or_exit(
            f"Found {len(config_users_and_roles)} users and roles in {input_file} - "
            f"{config_users_and_roles_sample}, ... - Continue?",
            yes,
        )

        users_to_update, users_to_add, users_to_delete, users_in_both = client.get_users_to_update_for_workspace(
            config_users_and_roles, workspace_id
        )

        echo_existing_users(users_in_both)

        update_users(client, users_to_update, workspace_id)

        add_users(client, users_to_add, workspace_id)

        delete_users(users_to_delete, client, workspace_id)


def echo_existing_users(users_in_both):
    if len(users_in_both):
        click.echo(f"Found {len(users_in_both)} users in both: {users_in_both}")


def update_users(client, users_to_update, workspace_id):
    if len(users_to_update) and click.confirm(
        f"Found {len(users_to_update)} users to update: {users_to_update} - Continue?"
    ):
        for user, role in users_to_update.items():
            click.echo(f"Updating user: {user} with role: {role}")
            client.update_workspace_user_with_role(user, role, workspace_id)


def add_users(client, users_to_add, workspace_id):
    if len(users_to_add) and click.confirm(f"Found {len(users_to_add)} users to add: {users_to_add} - Continue?"):
        for user, role in users_to_add.items():
            click.echo(f"Adding user: {user} with role: {role}")
            client.add_workspace_user_with_role(user, role, workspace_id)


if __name__ == "__main__":
    load_dotenv()
    cli(auto_envvar_prefix="astro_apply")
