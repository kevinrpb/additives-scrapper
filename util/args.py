import os
from argparse import ArgumentParser

from .log import get_level, setup_logger

def parse_args():
  logger = setup_logger(__name__)

  parser = ArgumentParser('additives-scrapper')

  parser.add_argument('start',
                      type=int,
                      default=5)

  parser.add_argument('end',
                      type=int,
                      default=500)

  parser.add_argument('-l', '--log-level',
                      type=str.lower,
                      choices=['debug', 'info', 'warning', 'error'],
                      default='warning')

  args = parser.parse_args()

  os.environ['LOG_LEVEL'] = f'{args.log_level}'
  args.log_level = get_level(args.log_level)

  logger = setup_logger(__name__)
  logger.debug('Parsed arguments')

  return args
