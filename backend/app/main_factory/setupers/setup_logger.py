from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler


log_dir = Path(__file__).resolve().parent.parent.parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)


def setup_logger(config):
    log_file_template = log_dir / Path(config.logger["file_name_template"])

    time_handler = TimedRotatingFileHandler(
        log_file_template,
        when=config.logger["timed_rotating_file_when"],
        interval=config.logger["interval"],
        encoding=config.logger["encoding"]
    )

    time_handler.setFormatter(logging.Formatter(config.logger["log_format"]))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            time_handler
        ]
    )
