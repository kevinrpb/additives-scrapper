
import logging


def setup_logger(level = logging.INFO):
  logger = logging.getLogger('additives-scrapper')
  logger.setLevel(level)

  # create console handler and set level to debug
  handler = logging.StreamHandler()
  handler.setLevel(level)

  # create formatter
  formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')

  # add formatter to handler
  handler.setFormatter(formatter)

  # add handler to logger
  logger.addHandler(handler)

  return logger
