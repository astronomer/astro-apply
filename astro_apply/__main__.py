from pathlib import Path

import click
import deepmerge
import yaml
from click import UsageError
from dotenv import load_dotenv
from gql.transport.exceptions import TransportQueryError

from astro_apply import (
    add_users,
    confirm_or_exit,
    delete_users,
    echo_existing_users,
    get_config_from_users_and_roles,
    houston_basedomain_to_api,
    update_users,
)
from astro_apply.client import CloudClient, SoftwareClient, get_users_to_update_for_workspace
from astro_apply.constants import ASTRO_CLOUD_API_URL, ASTRO_CLOUD_BASEDOMAIN, NEBULA_BASEDOMAIN_URL

d = {"show_default": True, "show_envvar": True}
fd = {"show_default": True, "show_envvar": True, "is_flag": True}
rp = {"prompt": True, "required": True}


class OptionPromptNull(click.Option):
    _value_key = "_default_val"

    def __init__(self, *args, **kwargs):
        self.default_option = kwargs.pop("default_option", None)
        super().__init__(*args, **kwargs)

    def get_default(self, ctx, **kwargs):
        if not hasattr(self, self._value_key):
            if self.default_option is None:
                default = super().get_default(ctx)
            else:
                arg = ctx.params[self.default_option]
                default = self.type_cast_value(ctx, self.default(arg))
            setattr(self, self._value_key, default)
        return getattr(self, self._value_key)

    def prompt_for_value(self, ctx):
        default = self.get_default(ctx)

        # only prompt if the default value is None
        if default is None:
            return super().prompt_for_value(ctx)

        return default


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
    cls=OptionPromptNull,
    default_option="yes",
    default=lambda x: x,
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
                text="Workspace Service Account Token", hide_input=True, type=str
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

        existing_users_and_roles = client.get_workspace_users_and_roles(workspace_id)

        users_to_update, users_to_add, users_to_delete, users_in_both = get_users_to_update_for_workspace(
            config_users_and_roles, existing_users_and_roles
        )

        echo_existing_users(users_in_both)

        update_users(client, users_to_update, workspace_id, yes)

        add_users(client, users_to_add, workspace_id, yes)

        delete_users(users_to_delete, client, workspace_id, yes)


if __name__ == "__main__":
    # https://click.palletsprojects.com/en/8.1.x/options/#values-from-environment-variables
    load_dotenv()
    cli(auto_envvar_prefix="ASTRO_APPLY")
