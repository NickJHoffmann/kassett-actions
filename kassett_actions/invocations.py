import os
import json

from kassett_actions.misc import clean_input
from kassett_actions.aws import extract_secrets
from kassett_actions.github import inject_to_environment, normalise_environment_variables


def write_aws_keys():
    keys = clean_input(os.environ["AWS_KEYS"])
    injections = extract_secrets(keys)
    return inject_to_environment(injections)


def normalise_environment_variables_for_kassett():
    inputs = json.loads(os.environ.get("KASSETT_INPUTS"))
    injections = normalise_environment_variables(inputs)
    return inject_to_environment(injections)
