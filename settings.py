import os

from dotenv import dotenv_values

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
CONFIG_PATH = env.get("ASTRO_CONFIG", "config.yaml")
