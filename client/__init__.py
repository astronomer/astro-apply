import copy
import itertools
import logging
import os
from copy import deepcopy
from typing import Dict, Optional, Tuple

from deepdiff import DeepDiff
from dotenv import dotenv_values
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

from client import houston_schema

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


def run(fn, is_mutation: bool = False, **kwargs):
    """
    Run graphql query or mutation against Houston API.
    Returns response as ORM
    """
    endpoint = HTTPEndpoint(URL, HEADERS)
    query = Operation(houston_schema.Mutation if is_mutation else houston_schema.Query)
    fn(query, **kwargs)
    data = endpoint(query)
    return query + data


def compare(
    current: Optional[Dict[str, dict]], new: Optional[Dict[str, dict]]
) -> Tuple[dict, dict, dict]:
    """
    Compares current values with values from config against current configuration.
    Returns a dict of items to add, a dict of items to update, and a dict of items to delete so
    they can be passed to Houston
    """

    current = current or {}
    new = new or {}

    add = copy.deepcopy(new)
    remove = copy.deepcopy(current)
    update = {}

    for key in list(new.keys()):
        if key in current:
            diff = DeepDiff(current[key], new[key])
            if diff:
                logging.debug(f"{new[key]}: {diff}")
                update[key] = new[key]
            add.pop(key)
            remove.pop(key)

    return add, update, remove


def apply_defaults(config):
    defaults = deepcopy(config)
    defaults.pop("deployments")

    for deployment, key in itertools.product(config["deployments"], defaults):
        for item in defaults[key]:
            if key not in deployment:
                deployment[key] = []
            if item not in deployment[key]:
                deployment[key].append(item)

    return config
