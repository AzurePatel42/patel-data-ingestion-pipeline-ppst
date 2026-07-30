import logging
import sys


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure application logging.

    This function should be called once during application startup.
    """

    root_logger = logging.getLogger()

    # Prevent duplicate handlers when running with reload=True
    if root_logger.handlers:
        return

    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        stream=sys.stdout,
    )