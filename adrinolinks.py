from cloudscraper import CloudScraper as Session
from proxyscrape import generate_random_ip
from limiter import *
import re

def run_adrino_bot(link, proxy=None, headless=None):
    # idn = 'urlbot-adrinolink'
    # if isCompleted(1249, idn): return print('Target Completed. Function did not run')
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    r1=s.get(link, headers={'Referer': 'https://filmyfly.tel/'}, allow_redirects=False)
    loc = r1.headers.get('Location')
    if loc is None:
        raise Exception(f'Error in adrino links. Location is None. Status: {r1.status_code}')
    print('Adrino Links:', loc)
    # submitOne(idn)
    


if __name__=='__main__':
    from all_links import random_adrino
    from proxyscrape import get_session
    print(random_adrino)
    run_adrino_bot(random_adrino, get_session(), headless=False)

