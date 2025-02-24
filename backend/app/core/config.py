from pathlib import Path

import yaml


class Config:
    """_summary_
    """

    def __init__(self, **entries) -> None:
        """_summary_
        """
        self.__dict__.update(entries)



config_dir = Path(__file__).resolve().parent.parent.parent / "config"

with open(config_dir / "config.yaml", "r") as file:
    config_dict = yaml.safe_load(file)


config = Config(**config_dict)
