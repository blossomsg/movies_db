"""Modules to read yaml files"""

from typing import Any, Dict, Optional

# pylint: disable=import-error
import yaml


def read_yaml_config(config: str, ext: str = ".yaml") -> Optional[Dict[str, Any]]:
    """This function reads the .yaml file.

    Args:
        config(str): .yaml configuration file.
        ext(str): .yaml extension.

    Returns:
        .yaml file data as dictionary else None

    """
    if config.endswith(ext):
        with open(config, "r", encoding="utf-8") as file:
            file_data = yaml.safe_load(file.read())
            if isinstance(file_data, Dict):
                return file_data
    return None
