from cloudscraper import CloudScraper as Session
from proxyscrape import get_session
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests, random
from time import sleep
from limiter import *

def getLink():
  s = Session()
  r = s.get('https://pico-stream.vercel.app/')
  doc = BeautifulSoup(r.text, 'html.parser')
  e = random.choice(doc.select('.item[href]'))
  unlockUrl = urljoin(r.url, e['href']) + '/unlock'
  apiUrl = 'https://arolinks.com/st?api=586850b580ee1e57b387721e1bc33e4c77f1f323&url=' + unlockUrl
  r = s.get(apiUrl)
  doc = BeautifulSoup(r.text, 'html.parser')
  data = dict(api='586850b580ee1e57b387721e1bc33e4c77f1f323', url=unlockUrl)
  for inp in doc.select('form input[name][value]'): data[inp['name']] = inp['value']
  r = s.post(apiUrl, data=data, allow_redirects=False)
  link = urljoin(apiUrl, r.headers.get('Location'))
  return link


def getRef(link='https://arolinks.com/14x', proxy=None):
  s = Session()
  s.proxies = dict(http=proxy, https=proxy)
  try:
    r = s.get(link, headers={'Referer': 'https://pico-stream.vercel.app/'}, allow_redirects=False, timeout=10)
  except requests.exceptions.ProxyError: getRef(link, proxy)
  if 'Turn off VPN' in r.text:
    raise Exception('IP Blocked. Using Proxy to get referer...')
  doc = BeautifulSoup(r.text, 'html.parser')
  ref = urljoin(r.url, doc.select_one('a[href]')['href']).split('verify.php')[0]
  return ref, r.cookies


def run_arolink_bot(proxy=None, headless=None):
    idn = 'urlbot-arolink'
    if random.choice([0, 0, 1]): return print('Randomly Function did not run.')
    if isCompleted(720, idn): return print('Target Completed. Function did not run.')
    link = getLink()
    try:
      rcData = getRef(link, proxy)
    except Exception as e:
      if 'IP Blocked' in str(e):
        print('IP is blocked. Using or changing proxy...')
        return run_arolink_bot(get_session())
    ref, cookies = rcData
    s = Session()
    s.proxies = dict(http=proxy, https=proxy)
    for c in cookies: s.cookies.set(c.name, c.value, domain=c.domain)
    s.cookies.set('ab', '2', domain='arolinks.com')
    r = s.get(link, headers={'Referer': ref})
    d = BeautifulSoup(r.text, 'html.parser')
    data = { i.get('name') : i.get('value') for i in d.select('#go-link input[name][value]')}
    sleep(int(d.select_one('#timer').text.strip()))
    r = s.post('https://arolinks.com/links/go', headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https:/arolinks.com', 'Referer': link}, data=data)
    if 'success' not in r.text: raise Exception('Error in AroLink: %s' % r.text)
    print('AroLink:', r.text)
    submitOne(idn)


if __name__ == '__main__':
  run_arolink_bot(get_session())
