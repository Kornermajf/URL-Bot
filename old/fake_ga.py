from cloudscraper import CloudScraper as Session
from proxyscrape import get_session
from urllib.parse import quote, quote_plus, urlparse
from time import time
from random import randint

pr = get_session()

def fake_ga(url : str, title : str, gid : str, proxy : str = None):
    s = Session()
    s.proxies = dict(http=proxy, https=proxy)
    BASE_URL = 'https://region1.google-analytics.com/g/collect?v=2&tid={GID}&gtm=45je4650v9180932424za200&_p={TIME1000}&gcd=1{GCD5}&npa=1&dma_cps=sypham&dma=1&tag_exp=0&cid={RAND9}.{TIME}&ul=en-us&sr=1366x768&uaa=x86&uab=64&uafvl=Google%2520Chrome%3B{VERSION}%7CChromium%3B{VERSION}%7CNot.A%252FBrand%3B{VERSION2}&uamb=0&uam=&uap=Windows&uapv=3.0.0&uaw=0&are=1&frm=0&pscdl=noapi&_s=1&sid={TIME}&sct=1&seg=0&dl={URL}&dt={TITLE}' \
                .replace('{TIME1000}', str(int(time()*1000))) \
                .replace('{GCD5}', 'l'.join(list(str(randint(11111, 99999))))) \
                .replace('{TIME}', str(int(time()))) \
                .replace('{RAND9}', str(randint(111111111, 999999999))) \
                .replace('{VERSION}', f'{randint(50, 150)}.{randint(1, 120)}.{randint(1111, 9999)}.{randint(111, 999)}') \
                .replace('{VERSION2}', f'{randint(1, 50)}.{randint(1, 18)}.{randint(1, 30)}.{randint(30, 86)}') \
                .replace('{URL}', quote_plus(url)) \
                .replace('{TITLE}', quote(title)) \
                .replace('{GID}', gid)

    netloc = urlparse(url).netloc
    for i in [f'&en=page_view&_fv=1&_nsi=1&_ss=1&_ee=1&tfd={randint(1111, 9999)}', f'&en=scroll&epn.percent_scrolled=90&_et=105&tfd={randint(11111, 99999)}']:
        s.post(BASE_URL + i, headers={"Origin": f"https://{netloc}", "Referer": f"https://{netloc}/"})

    return True

if __name__ == '__main__':
    fake_ga('https://www.flixwonders.com/',
            "Flix Wonders - Ultimate Big Bang of Movies",
            'G-V5D81QRWQ1',
            pr)
    # fake_ga('https://www.flixwonders.com/2021/12/spider-man-no-way-home.html',
    #         "Spider-Man: No Way Home - Flix Wonders",
    #         'G-V5D81QRWQ1',
    #         pr)

