"""Logging Configuration module."""
from logging import (
    Logger,
    StreamHandler,
    getLogger,
)

from pythonjsonlogger import jsonlogger

from service.commons.environment import (
    ENVIRONMENT,
    LOG_LEVEL,
    SERVICE_VERSION
)


def get_logger(name: str) -> Logger:
    """Get logger instance.

    Parameters
    ----------
    name : str
        Unique name for the logger instance

    Returns
    -------
    Logger
        Logger instance with JSON ouput
    """
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(module)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S.%s%z",
        rename_fields={
            "asctime": "@timestamp",
            "levelname": "level",
        },
        static_fields={
            "version": SERVICE_VERSION,
            "team": "Modelia",
            "environment": ENVIRONMENT,
        },
    )

    handler = StreamHandler()
    handler.formatter = formatter

    log = getLogger(name)
    log.addHandler(handler)
    log.setLevel(LOG_LEVEL)

    return log
