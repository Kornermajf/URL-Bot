from cloudscraper import CloudScraper as Session
from proxyscrape import generate_random_ip
from limiter import *
import re, threading, random

def google_view():
    Session().get('https://api.scrapingant.com/v2/general', params={'url': 'https://advicefunda.com', 'x-api-key': '4dfd9a009b6f4b92a8fbaf938986a358'})

def run_nano_bot(link, proxy=None, headless=None):
    idn = 'urlbot-nanolink'
    if isCompleted(2100, idn): return print('Target Completed. Function did not run')
    if random.randint(0, 1): return print('Randomly Function did not run')
    
    # threading.Thread(target=google_view).start()
    
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    r1=s.get(link, headers={'Referer': 'https://pico-stream.vercel.app/'}, allow_redirects=False)
    loc = r1.headers.get('Location')
    if loc is None:
        raise Exception(f'Error in nano links. Location is None. Status: {r1.status_code}')
    print('Nano Links:', loc)
    submitOne(idn)
    


if __name__=='__main__':
    from all_links import random_nanolinks
    from proxyscrape import get_session
    print(random_nanolinks)
    run_nano_bot(random_nanolinks, get_session(), headless=False)

