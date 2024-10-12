from cloudscraper import CloudScraper as Session
from proxyscrape import generate_random_ip
from limiter import *
import re, random, threading

def google_view():
    Session().get('https://api.scrapingant.com/v2/general', params={'url': 'https://www.flixwonders.com/2024/07/kill.html', 'x-api-key': '30a09c70e581413d9c067a3c0901448d'})

# threading.Thread(target=google_view).start()

def run_adrino_bot(link, proxy=None, headless=None):
    idn = 'urlbot-adrinolink'
    if isCompleted(1200, idn): return print('Target Completed. Function did not run')
    if random.randint(0, 1): return print('Randomly Function did not run')
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    r1=s.get(link, headers={'Referer': 'https://flixtor.guru/'}, allow_redirects=False)
    loc = r1.headers.get('Location')
    if loc is None:
        raise Exception(f'Error in adrino links. Location is None. Status: {r1.status_code}')
    print('Adrino Links:', loc)
    submitOne(idn)
    


if __name__=='__main__':
    from all_links import random_adrino
    from proxyscrape import get_session
    print(random_adrino)
    run_adrino_bot(random_adrino, get_session(), headless=False)

