import os
from typing import Dict


def inject_to_environment(variables: Dict[str, str]):
    lines = ["{}={}".format(k, v) for k, v in variables.items()]
    if os.environ.get("GITHUB_CI") is not None:
        env_file = os.getenv('GITHUB_ENV')
        with open(env_file, "a") as f:
            f.write("\n".join(lines))
    else:
        return lines


def normalise_environment_variables(inputs: Dict[str, str]):
    keys = [x for x in inputs.keys() if x.endswith("-env-name")]
    new_env_variables = {}
    banned_keys = []
    required = []

    for k in keys:
        new_key = k.replace("-env-name", "")
        var_name = "KASSETT_{}".format(new_key.upper().replace("-", "_"))
        required.append(var_name)
        if new_key in inputs and inputs[new_key] != '' and inputs[new_key] != "''":
            new_env_variables[var_name] = inputs[new_key]

        else:
            if inputs[k] is not None and inputs[k] in os.environ:
                new_env_variables[var_name] = os.environ[inputs[k]]
        banned_keys.append(new_key)
        banned_keys.append(k)

    new_env_variables["KASSETT_INPUTS"] = ""

    for k, v in inputs.items():
        if k not in banned_keys:
            if " " in v and not v.startswith("\""):
                v = '"{}"'.format(v)
            new_key = "KASSETT_{}".format(k.upper().replace("-", "_"))
            new_env_variables[new_key] = v

    for r in required:
        if r not in new_env_variables:
            new_env_variables[r] = ""
    return new_env_variables
