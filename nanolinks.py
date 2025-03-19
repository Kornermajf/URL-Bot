from cloudscraper import CloudScraper as Session
from proxyscrape import get_session
from DrissionPage import ChromiumPage, ChromiumOptions, errors
import re, threading, random, traceback
from time import sleep
from limiter import *


def run_nano_bot(link, proxy=None, headless=None):
    idn = 'urlbot-nanolink'
    if isCompleted(2100, idn): return print('Target Completed. Function did not run')
    if random.randint(0, 1): return print('Randomly Function did not run')
    
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    r1=s.get(link, headers={'Referer': 'https://pico-stream.vercel.app/'}, allow_redirects=False)
    loc = r1.headers.get('Location')
    if loc is None:
        raise Exception(f'Error in nano links. Location is None. Status: {r1.status_code}')
    print('Nano Links:', loc)
    submitOne(idn)
    
def run_nano_bot_browser():
    try:
        page = ChromiumPage(ChromiumOptions().set_argument('--start-maximized').auto_port().add_extension('./BusterExt'))
        oldPage = page
        page.get('https://hyperapks.xyz/wp-sitemap-posts-post-1.xml')
        link = random.choice(page.eles('css:.loc a')).attr('href')
        page.get('https://www.google.com')
        page.run_js(f"window.location.href='{link}'")
        page.wait.load_start(10, False)
        page.wait.doc_loaded()
        sleep(2)
        def scrollAllOver(speed = 1):
            page.run_js('window.scrollTo(0, 0)')
            totalHeight = page.run_js('return document.body.scrollHeight')
            currScroll = 0
            while currScroll < totalHeight:
                step = random.randint(50, 150) * speed
                page.actions.scroll(step)
                currScroll += step
                sleep(random.uniform(0.1, 1.5) / speed)
        scrollAllOver(1.8)
        page.wait.ele_displayed('css:.downloadAPK.dapk_b')
        page.ele('css:.downloadAPK.dapk_b', timeout=10).click()
        sleep(0.5)
        page = page.latest_tab
        page.wait.doc_loaded()
        while 1:
            sleep(1)
            if not 'Just a moment' in page.title: break
        sleep(3)
        while 'Bot Verification' in page.title:
            iframe = page.ele('css:iframe[title="reCAPTCHA"]')
            iframe.ele('css:#rc-anchor-container span[role="checkbox"]').click()
            iframe = page.ele('css:iframe[title="recaptcha challenge expires in two minutes"]')
            iframe.ele('css:div.button-holder.help-button-holder').shadow_root.ele('#solver-button').click()
            sleep(10)
        page.wait.doc_loaded()
        try: page.ele('css:.fc-cta-consent').click()
        except Exception as err:
            if 'No element' in str(err): pass
        sleep(1)
        scrollAllOver()
        try: page.ele('css:#popup .close').click()
        except: pass
        link = re.findall(r'window\.location\.href\s*=\s*"([^"]+)"', page.html)[0].strip()
        pr = get_session()
        r = Session().get(link, headers={'Referer': page.url}, proxies=dict(http=pr, https=pr), allow_redirects=False)
        rLink = r.headers.get('Location')
        print('NanoLinks:', rLink)
        oldPage.quit()
    except Exception as err:
        ss = oldPage.get_screenshot(as_bytes=True, full_page=True)
        url = Session().post('https://freeimage.host/api/1/upload', params=dict(key='6d207e02198a847aa98d0a2a901485a5'), files=dict(source=ss)).json().get('image', {}).get('url')
        raise Exception(traceback.format_exc() + '\n\nScreenshot: ' + url)





if __name__=='__main__':
    # from all_links import random_nanolinks
    # run_nano_bot(random_nanolinks, get_session(), headless=False)
    run_nano_bot_browser()

