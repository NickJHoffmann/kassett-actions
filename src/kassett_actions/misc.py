import json
from typing import List


def coalesce(*args):
    for arg in args:
        if arg is not None:
            return arg
    return None


def valid_json(obj: str):
    try:
        json.loads(obj)
    except ValueError:
        return False
    return True


def clean_input(payload: str) -> List[str]:
    payload = payload.replace("\n", "")
    response = []
    secrets = payload.split(",")
    for secret in secrets:
        response.append(secret.strip())
    return response
