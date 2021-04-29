#!/bin/sh

. .env
if [ "$NO_DOWNLOAD" != 1 ]; then
    if [ -z "$TOKEN" ]; then
        echo "please export TOKEN with your Astronomer API token" >&2
        echo "see: https://app.$BASEURL/tokens or use a service account token" >&2
        exit 1
    fi

    URL=https://houston.$BASEURL/v1
    echo "Fetching schema from ${URL}..."
    python \
        -m sgqlc.introspection \
        -H "Authorization: bearer ${TOKEN}" \
        "$URL" \
        houston_schema.json || exit 1
    echo "Fetched!"
fi

sgqlc-codegen schema \
  --docstrings \
  houston_schema.json houston_schema.py || exit 1

#sgqlc-codegen operation \
#  --schema houston_schema.json \
#  houston_schema \
#  houston_operations.py \
#  houston_schema.graphql || exit 1