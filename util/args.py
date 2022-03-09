import logging
from argparse import ArgumentParser

logger = logging.getLogger('additives-scrapper')

def parse_args():
  def get_level(level_str: str) -> int:
    m = {
      'debug': logging.DEBUG,
      'info': logging.INFO,
      'warning': logging.WARNING,
      'error': logging.ERROR
    }

    return m[level_str]

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

  logger.debug('Parsing arguments')
  args = parser.parse_args()
  args.log_level = get_level(args.log_level)

  return args
