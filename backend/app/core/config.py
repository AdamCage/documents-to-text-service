from pathlib import Path

from utils.files_handlers import load_yaml


class Config:
    """_summary_
    """

    def __init__(self, **entries) -> None:
        """_summary_
        """
        self.__dict__.update(entries)



config_dir = Path(__file__).resolve().parent.parent.parent / "config"
config_dict = load_yaml(config_dir / "config.yaml")

config = Config(**config_dict)
http_format = "http" if config.cert_path is None else "https"
