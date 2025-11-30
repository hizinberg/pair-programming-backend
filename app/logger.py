import logging
import sys

'''Logging configuration for the application.
'''

formatter = logging.Formatter(
    "%(levelname)-8s | %(asctime)s | %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False
