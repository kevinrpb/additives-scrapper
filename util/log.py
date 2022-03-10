
import logging
import os


def get_level(level_str: str) -> int:
  m = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR
  }

  return m[level_str]

def setup_logger(name: str = 'additives-scrapper', level = None):
  if level is None:
    if 'LOG_LEVEL' in os.environ.keys():
      level = get_level(os.environ['LOG_LEVEL'])
    else:
      level = logging.INFO

  logger = logging.getLogger(name)
  logger.setLevel(level)

  # create console handler and set level to debug
  handler = logging.StreamHandler()
  handler.setLevel(level)

  # create formatter
  formatter = logging.Formatter('[%(asctime)s] [%(levelname)7s] [%(name)25s] %(message)s')

  # add formatter to handler
  handler.setFormatter(formatter)

  # add handler to logger
  logger.addHandler(handler)

  return logger
