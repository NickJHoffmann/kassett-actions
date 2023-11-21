import json
import boto3
from typing import List

from kassett_actions.misc import valid_json, coalesce


class Secret(object):
    def __init__(
            self,
            env_name: str = None,
            env_name_prefix: str = None,
            secret_name: str = None,
            secret_name_prefix: str = None,
    ):
        self.env_name = env_name
        self.env_name_prefix = env_name_prefix
        self.secret_name = secret_name
        self.secret_name_prefix = secret_name_prefix
        self.arn = None

    def resolve(self, client):
        put = {}
        value = client.get_secret_value(SecretId=self.arn)
        secret_string = json.loads(value["SecretString"])
        prefix = coalesce(self.env_name, self.env_name_prefix, "")
        if valid_json(value["SecretString"]):
            for k, v in secret_string.items():
                k = prefix + k.upper().replace("-", "_")
                put[k] = v
        else:
            put[
                coalesce(
                    self.env_name,
                    self.env_name_prefix,
                    value["Name"].upper().replace("-", "_")
                )
            ] = value["SecretString"]
        return put


def _potential_secret(obj: str):
    temp = {}
    if "=" in obj:
        t = obj.split("=")
    else:
        t = ["", obj]
    if t[1].endswith("*"):
        temp["secret_name_prefix"] = t[1][0:-1]
    else:
        temp["secret_name"] = t[1]
    if t[0].endswith("*"):
        temp["env_name_prefix"] = t[0][0:-1]
    else:
        if t[0] != "":
            temp["env_name"] = t[0]
    return Secret(**temp)


def map_secret_arns(paginator, secrets: List[Secret]):
    for page in paginator.paginate():
        for name in page['SecretList']:
            i = next((i for i, x in enumerate(secrets) if x.secret_name is not None and x.secret_name == name["Name"]), None)
            if i is not None:
                secrets[i].arn = name["ARN"]
            i = next((i for i, x in enumerate(secrets) if x.secret_name_prefix in x and name["Name"].startswith(x.secret_name_prefix)), None)
            if i is not None:
                secrets[i].arn = name["ARN"]


def extract_secrets(secrets: List[str]):
    secrets_to_retrieve: List[Secret] = []
    for i in secrets:
        secrets_to_retrieve.append(_potential_secret(i))

    client = boto3.client('secretsmanager')
    paginator = client.get_paginator('list_secrets')
    map_secret_arns(paginator, secrets_to_retrieve)
    return {key: value for d in secrets_to_retrieve for key, value in d.resolve(client).items()}