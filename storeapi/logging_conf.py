from logging.config import dictConfig

from .config import DevConfig, config


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(name)s:%(lineno)d - %(message)s",
                }
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                }
            },
            "loggers": {
                "uvicorn": {"handlers": ["default"], "level": "INFO"},
                # root is the parent of all
                # storeapi.routers.post
                "storeapi": {
                    "handlers": ["default"],
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    # root is out
                    # we do not want to use it in dev
                    "propagate": False,
                },
                "databases": {"handlers": ["default"], "level": "WARNING"},
                "aiosqlite": {"handlers": ["default"], "level": "WARNING"},
            },
        }
    )
