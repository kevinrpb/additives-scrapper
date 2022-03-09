
import requests
from bs4 import BeautifulSoup

from util.log import setup_logger

from .hacks import cleanup_text

__cookies_url = 'https://webgate.ec.europa.eu/foods_system/main/index.cfm?sector=FAD&auth=SANCAS'
__session = requests.Session()
__session.cookies.update({
  'eu_cookie_consent': '%7B%22a%22%3A%7B%22europa%22%3A%5B%22europa-analytics%22%2C%22load-balancers%22%2C%22authentication%22%5D%7D%2C%22r%22%3A%7B%7D%7D'
})
def get_page(url: str) -> BeautifulSoup:
  logger = setup_logger(__name__)

  # Setup cookies first
  if 'JSESSIONID' not in __session.cookies.keys():
    logger.debug('Generating initial cookies')
    response = __session.get(__cookies_url)
    __session.cookies.update(response.cookies)

  # Then fetch page
  page = __session.get(url)
  html = cleanup_text(page.text)

  # And parse it
  soup = BeautifulSoup(html, 'lxml')

  return soup
