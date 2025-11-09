import logging
import sys
from typing_extensions import override

GREY = "\x1b[38;21m"
BLUE = "\x1b[38;5;39m"
YELLOW = "\x1b[38;5;226m"
RED = "\x1b[38;5;196m"
BOLD_RED = "\x1b[31;1m"
RESET = "\x1b[0m"

BASE_FMT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"

LEVEL_FORMATS = {
    logging.DEBUG: GREY + BASE_FMT + RESET,
    logging.INFO: BLUE + BASE_FMT + RESET,
    logging.WARNING: YELLOW + BASE_FMT + RESET,
    logging.ERROR: RED + BASE_FMT + RESET,
    logging.CRITICAL: BOLD_RED + BASE_FMT + RESET,
}


class CustomFormatter(logging.Formatter):
    @override
    def format(self, record: logging.LogRecord) -> str:
        log_fmt = LEVEL_FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, DATE_FMT)
        return formatter.format(record)


def setup_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)

    fmt = CustomFormatter()
    handler.setFormatter(fmt)
    root.addHandler(handler)
