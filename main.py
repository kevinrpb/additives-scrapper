#!/usr/bin/env python3

import json

from scrappers import EAditivosScrapper, EuropaScrapper, LaVeganisteriaScrapper
from util import parse_args, select_dietary, setup_logger, update_dietary


def main():
  args = parse_args()
  logger = setup_logger(level=args.log_level)
  logger.info('Starting')

  # Get the scrappers ready
  europa_scrapper = EuropaScrapper()
  eaditivos_scrapper = EAditivosScrapper()
  laveganisteria_scrapper = LaVeganisteriaScrapper()

  # Get the information
  additives_info = europa_scrapper.get_additives(args.start, args.end)
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

  # See which numbers we get
  numbers = map(lambda element: element['number'], additives_info)

  # Get some dietary information from several sources
  dietary_info = eaditivos_scrapper.get_additives()
  dietary_info = update_dietary(dietary_info, laveganisteria_scrapper.get_additives())
  # returns a dict of
  # {
  #   number: {
  #     'vegetarian': ...
  #     'vegan': ...
  #   }
  # }

  # Consolidate the dietary info and update the original base with it
  dietary_info = select_dietary(dietary_info)
  for index, element in enumerate(additives_info):
    e_id = element['number']

    if e_id in dietary_info.keys():
      additives_info[index]['dietary'].update(dietary_info[e_id])

  # Now save the json file
  logger.info('Done')
  logger.info('Saving additives to file...')
  with open('additives.json', 'w') as file:
    json.dump(additives_info, file, indent=2)

if __name__ == '__main__':
  main()
