from bs4 import BeautifulSoup, Tag
from util import get_page, setup_logger

logger = setup_logger(__name__)

class EAditivosScrapper:
  # *
  # * MARK: Config -
  # *

  BASE_URL = 'https://e-aditivos.com'

  # *
  # * MARK: Init -
  # *

  def __init__(self):
    self.logger = setup_logger(__name__)
    self.additives = {}

    self.__parse_web()

  # *
  # * MARK: HTML Parsing -
  # *

  def __parse_web(self):
    self.logger.debug('Parsing additives')

    vegetarian_ids = self.__pase_vegetarians()

    page: BeautifulSoup = get_page(self.BASE_URL)
    rows = (page.find(id='chems')
              .findChild('table', recursive=False)
              .findChild('tbody', recursive=False)
              .findChildren('tr', recursive=False))

    additives = {}
    for row in rows:
      e_id = row.findChild('td', { 'class': 'e-id' }).get_text().strip().replace('-', '')
      self.logger.debug(f'Parsing additive with id={e_id:5s}')

      e_source = row.findChild('td', { 'class': 'e-source' }).get_text().strip().lower()

      vegetarian = 'unknown'
      vegan = 'unknown'
      if e_source == 'vegetal':
        vegetarian = 'always'
        vegan = 'always'
      elif e_source == 'animal':
        vegan = 'never'
      else:
        if e_id in vegetarian_ids:
          vegetarian = 'always'

      self.logger.debug('    - Got info')
      self.logger.debug('    ┌')
      self.logger.debug(f'    │ vegetarian: {vegetarian}')
      self.logger.debug(f'    │ vegan: {vegan}')
      self.logger.debug('    └')

      additives[e_id] = {
        'vegetarian': vegetarian,
        'vegan': vegan
      }

    self.additives = additives

  def __pase_vegetarians(self):
    page: BeautifulSoup = get_page(f'{self.BASE_URL}/Vegetarianos')
    rows = (page.find(id='chems')
              .findChild('table', recursive=False)
              .findChild('tbody', recursive=False)
              .findChildren('tr', recursive=False))

    e_ids = []
    for row in rows:
      e_id = row.findChild('td', { 'class': 'e-id' }).get_text().strip().replace('-', '')

      e_ids.append(e_id)

    return e_ids

  # *
  # * MARK: Main -
  # *

  def get_additive(self, number: str) -> dict:
    self.logger.debug(f'Checking additive with id={id:04d}')

    if number in self.additives.keys():
      return self.additives[number]
    else:
      return {
        'vegetarian': 'unknown',
        'vegan': 'unknown'
      }

  def get_additives(self):
    self.logger.debug('Return all additives')

    return self.additives
