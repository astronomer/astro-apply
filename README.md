# astroctl

## Usage
This script takes a `config.yaml` file, fetches the Houston GraphQL Schema, parses the `config.yaml` file and attempts to apply the configuration via GraphQL against Houston

## Dev
- `houston_schema.json` and `houston_schema.graphql` are both downloaded from the Prism GraphQL interface. Need to figure out a way to automate this
- For convenience, we use .env file to get the $BASEURL and $TOKEN. You can get the token from https://app.<base-url>/token or use a Service Account token
- `config.yaml` is the default, but a different filename and path can be supplied via the `ASTRO_CONFIG` env var
- For dev/testing purposes, if you want to include a .env file while building a new image, make sure to comment out `.env` from `.dockerignore`
- To execute tests locally, run `python -m pytest`
