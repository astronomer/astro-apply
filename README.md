# astro-apply

## Usage
This script parses a `config.yaml` file and attempts to apply the configuration via GraphQL against Houston, allowing teams to manage their airflow deployments in a git-ops manner. Users declare the desired state in the config file, and the tool will compare against the current configuration, and apply changes where needed. It is meant to be used as part of a cicd process, but can be used standalone if needed

## Dev
- `houston_schema.json` and `houston_schema.graphql` are both downloaded from the Prism GraphQL interface, and a python ORM `houston_schema.py` is generated from this. To update the ORM, run the script in `update_schema.sh`
- For convenience, we use .env file to get the $BASEURL and $TOKEN. You can get the token from https://app.<base-url>/token or use a Service Account token
- `config.yaml` is the default, but a different filename and path can be supplied via the `ASTRO_CONFIG` env var
- For dev/testing purposes, if you want to include a .env file while building a new image, make sure to comment out `.env` from `.dockerignore`
- To execute tests locally, run `python -m pytest`
