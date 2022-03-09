
import logging

from bs4 import BeautifulSoup, Tag

from util import get_page


class EuropaScrapper:
  # *
  # * MARK: Config -
  # *

  BASE_URL = 'https://webgate.ec.europa.eu/foods_system/main/index.cfm?event=substance.view&identifier={}'

  # *
  # * MARK: Init -
  # *

  def __init__(self):
    pass

  # *
  # * MARK: HTML Parsing -
  # *

  # MARK: Parse General Data
  def __parse_general(self, main_content: Tag):
    table = (main_content.find('div', { 'class': 'BlocA' })
                        .find('div', { 'class': 'body' })
                        .find('div', { 'class': 'BoxB' }, recursive=False)
                        .find('div', { 'class': 'body' })
                        .find('table', { 'class': 'form'}))

    even_trs = table.find_all('tr', { 'class': 'even' })
    odd_trs = table.find_all('tr', { 'class': 'odd' })

    # This text is something like "Group III, Colours with combined maximum limit (Group III)"
    group_text = odd_trs[-1].find('td').get_text().strip()
    # print(group_text)

    # Sometimes the group is not present...
    if group_text is None or group_text == 'No':
      groups = []
    # Some identifiers refer to whole groups (like 150a-d), let's not use those
    elif group_text == 'Yes':
      return None
    elif '\n' in group_text:
      groups = group_text.split('\n')
    # When we have a group, use regex to get it
    else:
      groups = [group_text]

      # matches = re.findall(r'\(Group (.*)\)', group_text)
      # if len(matches) > 0:
      #   groups = [matches[0]]
      # else:
      #   groups = [group_text]

    name = even_trs[0].find('td').get_text().strip()
    number = even_trs[1].find('td').get_text().strip().replace(' ', '')
    synonyms = odd_trs[1].find('td').get_text().strip().split(',')
    # Somehow we end up with an empty synonym
    synonyms = list(filter(lambda item: item != '', synonyms))

    return {
      'number': number,
      'name': name,
      'synonyms': synonyms,
      'groups': groups
    }

  # MARK: Parse Authorisations of Use
  def __parse_authorisations(self, main_content: Tag):
    def parse_table(table: Tag):
      tr_odd = table.find('tr', { 'class': 'odd' })
      tr_even = list(filter(
        lambda tr: len(tr.find_all('td')) < 2,
        table.find_all('tr', { 'class': 'even' }, recursive=False)
      ))

      # Get the authorised foods
      food_items = tr_odd.find('ul').find_all('li')
      foods = list(map(lambda i: i.find('a').get_text().strip(), food_items))

      # Get the exceptions
      exceptions = list(map(lambda i: i.find('td').get_text().strip(), tr_even))
      exceptions = list(filter(lambda item: item != '', exceptions))

      return {
        'foods': foods,
        'exceptions': exceptions
      }

    boxA = (main_content.find('div', { 'class': 'BlocA' })
                          .find('div', { 'class': 'body' })
                          .find('div', { 'class': 'BoxA' }, recursive=False))

    if boxA is None:
      return []

    tables = (boxA
                .find('div', { 'class': 'body' })
                .find_all('table', { 'class': 'form'}))

    return list(map(parse_table, tables))

  # *
  # * MARK: Main -
  # *

  def get_additive(self, id: str) -> dict:
    logger = logging.getLogger('additives-scrapper')
    logger.info(f'Fetching additive with id={id:04d}')

    url = self.BASE_URL.format(id)
    page: BeautifulSoup = get_page(url)

    main_content = page.find(id='mainContent')

    # This element has no data or doesn't exist
    if main_content.find('div', { 'class': 'BlocA' }) is None:
      logger.warning('    - No data for this item, it probably doesn\' exist')
      return None

    general_data = self.__parse_general(main_content)
    if general_data is None:
      logger.warning('    - No general info for this item, must be a group')
      return None
    logger.debug('    - Got general info')
    logger.debug('    ┌')
    logger.debug(f'    │ number: {general_data["number"]}')
    logger.debug(f'    │ name: {general_data["name"]}')
    logger.debug(f'    │ synonyms: {general_data["synonyms"]}')
    logger.debug(f'    │ groups: {general_data["groups"]}')
    logger.debug('    └')

    authorisations = self.__parse_authorisations(main_content)
    logger.debug('    - Got authorisations')
    for authorisation in authorisations:
      logger.debug('    ┌')
      logger.debug(f'    │ foods: {authorisation["foods"]}')
      logger.debug(f'    │ exceptions: {authorisation["exceptions"]}')
      logger.debug('    └')

    return {
      'id': id,
      'number': general_data['number'],
      'name': general_data['name'],
      'synonyms': general_data['synonyms'],
      'groups': general_data['groups'],
      'dietary': {
        'vegetarian': 'unknown',
        'vegan': 'unknown'
      },
      'authorisations': authorisations
    }

  def get_additives(self, start, end):
    return list(
      filter(lambda i: i is not None, map(self.get_additive, range(start, end+1)))
    )
