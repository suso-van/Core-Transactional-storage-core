import yaml
import os

def load_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    # env override
    env = os.getenv("MINIDB_ENV")
    if env:
        env_path = f"config/{env}.yaml"
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                env_cfg = yaml.safe_load(f)
            deep_merge(config, env_cfg)

    # secrets
    secrets_path = "config/secrets.yaml"
    if os.path.exists(secrets_path):
        with open(secrets_path, "r") as f:
            secrets = yaml.safe_load(f)
        config["secrets"] = secrets.get("secrets", {})

    return config

def deep_merge(base, override):
    for k, v in override.items():
        if isinstance(v, dict) and k in base:
            deep_merge(base[k], v)
        else:
            base[k] = v
