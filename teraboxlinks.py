from DrissionPage import ChromiumPage, ChromiumOptions, errors
import re, random, traceback, json, atexit, subprocess, socket
from cloudscraper import CloudScraper as Session
from proxyscrape import generate_random_ip
from proxyscrape import get_session
from bs4 import BeautifulSoup
from time import sleep
from limiter import *

def run_terabox_bot(link, proxy=None, headless=None):
    # idn = 'urlbot-terabox'
    # if isCompleted(1428, idn): return print('Target Completed. Function did not run')
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    r1=s.get(link, headers={'Referer': 'https://pico-stream.vercel.app/'}, allow_redirects=False, stream=True)
    loc = r1.headers.get('Location')
    if loc is None:
        raise Exception('Error in teraboxlinks links. Location is None')
    print('TeraBox Links:', loc)
    # submitOne(idn)

pr = get_session()
USER, PASS, HOST, PORT = re.findall(r'^[^:]+:\/\/([^:]+):([^@]+)@([^:]+):(\d+)$', pr)[0]
p = subprocess.Popen(f'mitmdump --mode upstream:http://{HOST}:{PORT} --upstream-auth {USER}:{PASS} --listen-port 5858'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
atexit.register(p.kill)
while 1:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        if s.connect_ex(('127.0.0.1', 5858)) == 0: break
    sleep(1)

  
def run_tera_bot_browser():
    try: page = ChromiumPage(ChromiumOptions().set_argument('--start-maximized').set_argument('--ignore-certificate-errors').auto_port().add_extension('./ProxyExt'))
    except: page = ChromiumPage(ChromiumOptions().set_argument('--start-maximized').set_argument('--ignore-certificate-errors').auto_port().add_extension('./ProxyExt'))
    try:
        oldPage = page
        isQuit = False
        link = random.choice(json.load(open('post_links.json')))
        page.get(f'https://{random.choice(["google.com", "google.com", "facebook.com", "instagram.com", "bing.com", "bing.com"])}/robots.txt')
        page.run_js(f"window.location.href='{link}'")
        page.wait.load_start(10, False)
        page.wait.doc_loaded()
        sleep(2)
        def scrollAllOver(speed = 1):
            page.run_js('window.scrollTo(0, 0)')
            totalHeight = page.run_js('return document.body.scrollHeight')
            currScroll = 0
            while currScroll < totalHeight:
                totalHeight = page.run_js('return document.body.scrollHeight')
                step = random.randint(50, 150) * speed
                page.actions.scroll(step)
                currScroll += step
                sleep(random.uniform(0.1, 1.5) / speed)
        scrollAllOver(2)
        for i in range(10+1):
            try:
                page.ele('css:.downloadAPK.dapk_b', timeout=10).click(by_js=True)
                break
            except errors.NoRectError as err:
                if i == 10: raise err
                sleep(1)
        sleep(1)
        page = page.latest_tab
        page.wait.doc_loaded()
        while 'Just a moment' in page.title: sleep(3)
        page.wait.doc_loaded()
        sleep(3)
        page.run_js('''setInterval(()=>{document.querySelector('.fc-cta-consent')?.click()}, 1000)''')
        for i in range(10+1):
            try: page.ele('css:.fc-cta-consent').click();break
            except: pass
        sleep(3)
        scrollAllOver()
        ref = page.url
        furl = page.ele('#tp-snp2').attr('href')
        oldPage.quit()
        isQuit = True

        r = Session().get(furl, headers={'Referer': ref, 'Origin': f'https://{ref.split("/")[2]}'}, allow_redirects=False, stream=True, proxies=dict(http=pr, https=pr))
        loc = r.headers.get('Location')
        if not loc: raise Exception('Error is teraboxlinks. No location found.')
        print('Terabox Links:', loc)
    except Exception as err:
        if isQuit: raise err
        else:
            ss = page.get_screenshot(as_bytes=True, full_page=True)
            url = Session().post('https://freeimage.host/api/1/upload', params=dict(key='6d207e02198a847aa98d0a2a901485a5'), files=dict(source=ss)).json().get('image', {}).get('url')
            raise Exception(traceback.format_exc() + '\n\nScreenshot: ' + url)


if __name__=='__main__':
    # from all_links import random_teraboxlinks
    # from proxyscrape import get_session
    # print(random_teraboxlinks)
    # run_terabox_bot(random_teraboxlinks, get_session(), headless=False)
    run_tera_bot_browser()


