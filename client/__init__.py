import copy
import os
from typing import Optional, Dict, Tuple

from deepdiff import DeepDiff
from dotenv import dotenv_values
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

from client import houston_schema as schema


REQUIRED_VARS = [
    "BASEURL",  # e.g.  astro.mydomain.com
    "TOKEN",  # either a service account token or a temporary one obtained from app.BASEURL/token
]
env = {**dotenv_values(".env"), **os.environ}

for var in REQUIRED_VARS:
    if var not in env:
        raise SystemExit(f"Required env var {var} not found! Exiting!")

URL = f'https://houston.{env["BASEURL"]}/v1'
HEADERS = {"Authorization": env["TOKEN"]}
CONFIG_FILE = env.get("ASTRO_CONFIG", "config.yaml")


def run(fn, is_mutation: bool = False, **kwargs):
    """
    Run graphql query or mutation against Houston API.
    Returns response as ORM
    """
    endpoint = HTTPEndpoint(URL, HEADERS)
    query = Operation(schema.Mutation if is_mutation else schema.Query)
    fn(query, **kwargs)
    return query + endpoint(query)


def compare(
    current: Optional[Dict[str, dict]], new: Optional[Dict[str, dict]]
) -> Tuple[dict, dict]:
    """
    Compares current values with values from config against current configuration.
    Returns a dict of items to add, and a dict of items to delete so they can be passed to Houston
    """

    current = current or {}
    new = new or {}

    add = copy.deepcopy(new)
    remove = copy.deepcopy(current)

    for key in list(new.keys()):
        if key in current and not DeepDiff(
            current[key], new[key]
        ):
            add.pop(key)
            remove.pop(key)

    return add, remove
