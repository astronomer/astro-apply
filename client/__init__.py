import copy
import itertools
import logging
from copy import deepcopy
from typing import Dict, Optional, Tuple

from deepdiff import DeepDiff
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

from client import houston_schema
from settings import URL, HEADERS


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


def parse_from_config(key, section):
    return {
        item[key]: item for item in section
    }
