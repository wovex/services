import logging
import sys
from fastapi.logger import logger as fastapi_logger


handler = logging.StreamHandler(sys.stdout)
fastapi_logger.setLevel(logging.DEBUG)
fastapi_logger.addHandler(handler)
