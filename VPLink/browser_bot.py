import os, sys
DIR = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(DIR, '..'))
sys.path.insert(0, parent_dir)

from DrissionPage import ChromiumOptions, ChromiumPage, errors
import json, random, traceback, re
from cloudscraper import CloudScraper as Session
from time import sleep
from modify_req import runProxyServer


PORT = runProxyServer()

def run_browser():
    try: page = ChromiumPage(ChromiumOptions().set_argument('--start-maximized').set_argument('--ignore-certificate-errors').auto_port().set_proxy(f'http://127.0.0.1:{PORT}'))
    except: page = ChromiumPage(ChromiumOptions().set_argument('--start-maximized').set_argument('--ignore-certificate-errors').auto_port().set_proxy(f'http://127.0.0.1:{PORT}'))
    try:
        oldPage = page
        isQuit = False
        link = random.choice(json.load(open('post_links.json')))
        page.get(f'https://{random.choice(["google.com", "google.com", "facebook.com", "bing.com", "bing.com"])}/robots.txt')
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
        page = oldPage.latest_tab
        page.wait.doc_loaded()

        for x in range(1, 2 + 1):
            sleep(15)
            for i in range(10+1):
                try:
                    ebtn = page.ele('css:#tp-snp2, #btn7', timeout=10)
                    ebtn.click(by_js=True)
                    break
                except errors.NoRectError as err:
                    if i == 10: raise err
                    sleep(1)
            sleep(2)
            page = oldPage.latest_tab
            page.wait.doc_loaded()

        while 'vplink.in' not in page.url:
            sleep(3)
            page = oldPage.latest_tab

        page.wait.doc_loaded()
        print(page.ele('css:#timer').text)

        sleep(30)
        oldPage.quit()
        isQuit = True
    except Exception as err:
        if isQuit: raise err
        else:
            ss = page.get_screenshot(as_bytes=True, full_page=True)
            url = Session().post('https://freeimage.host/api/1/upload', params=dict(key='6d207e02198a847aa98d0a2a901485a5'), files=dict(source=ss)).json().get('image', {}).get('url')
            # oldPage.quit()
            raise Exception(traceback.format_exc() + '\n\nScreenshot: ' + url)


if __name__ == '__main__':
    run_browser()

