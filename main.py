#!/usr/bin/env python3

import json

from scrappers.europa import EuropaScrapper

from util import parse_args, setup_logger


def main():
  args = parse_args()
  logger = setup_logger(level=args.log_level)

  base_scrapper = EuropaScrapper()

  info = base_scrapper.get_additives(args.start, args.end)

  logger.info('Saving additives to file...')
  with open('additives.json', 'w') as file:
    json.dump(info, file, indent=2)

if __name__ == '__main__':
  main()
