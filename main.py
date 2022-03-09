#!/usr/bin/env python3

import json

from scrappers import EAditivosScrapper, EuropaScrapper
from util import parse_args, setup_logger

def main():
  args = parse_args()
  logger = setup_logger(level=args.log_level)
  logger.info('Starting')

  europa_scrapper = EuropaScrapper()
  europa_info = europa_scrapper.get_additives(args.start, args.end)
  # returns an array of
  # {
  #   'id': ...,
  #   'number': ...,
  #   'name': ...,
  #   'synonyms': ...,
  #   'groups': ...,
  #   'dietary': {
  #     'vegetarian': 'unknown',
  #     'vegan': 'unknown'
  #   },
  #   'authorisations': ...
  # }

  numbers = map(lambda element: element['number'], europa_info)

  eaditivos_scrapper = EAditivosScrapper()
  eaditivos_info = eaditivos_scrapper.get_additives()
  # returns a dict of
  # {
  #   number: {
  #     'vegetarian': ...
  #   }
  # }

  for index, element in enumerate(europa_info):
    e_id = element['number']

    if e_id in eaditivos_info.keys():
      europa_info[index]['dietary'].update(eaditivos_info[e_id])

  logger.info('Done')
  logger.info('Saving additives to file...')
  with open('additives.json', 'w') as file:
    json.dump(europa_info, file, indent=2)

if __name__ == '__main__':
  main()
