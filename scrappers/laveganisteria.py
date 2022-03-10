from bs4 import BeautifulSoup, Tag
from util import get_page, setup_logger

logger = setup_logger(__name__)

class LaVeganisteriaScrapper:
  # *
  # * MARK: Config -
  # *

  BASE_URL = 'https://www.laveganisteria.com/aditivos-alimentarios/'

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

    page: BeautifulSoup = get_page(self.BASE_URL)
    rows = page.find_all('div', { 'class': 'vc_tta-panel' })

    additives = {}
    for row in rows:
      e_id = row.findChild('span', { 'class': 'vc_tta-title-text' }).get_text().strip().split(' ')[0]
      self.logger.debug(f'Parsing additive with id={e_id:5s}')

      icon_classes = row.findChild('i', { 'class': 'vc_tta-icon' }).attrs['class']

      vegan = 'unknown'

      if 'fa-check-circle' in icon_classes:
        vegan = 'always'
      elif 'fa-question-circle' in icon_classes:
        vegan = 'sometimes'
      elif 'fa-times-circle' in icon_classes:
        vegan = 'never'

      self.logger.debug('    - Got info')
      self.logger.debug('    ┌')
      self.logger.debug(f'    │ vegan: {vegan}')
      self.logger.debug('    └')

      additives[e_id] = {
        'vegetarian': 'unknown',
        'vegan': vegan
      }

    self.additives = additives

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
