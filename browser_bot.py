from DrissionPage import ChromiumOptions, ChromiumPage, errors
import subprocess, atexit, socket, re, json, random, traceback
from cloudscraper import CloudScraper as Session
from proxyscrape import get_session
from bs4 import BeautifulSoup
from time import sleep


pr = get_session()
USER, PASS, HOST, PORT = re.findall(r'^[^:]+:\/\/([^:]+):([^@]+)@([^:]+):(\d+)$', pr)[0]
p = subprocess.Popen(f'mitmdump --mode upstream:http://{HOST}:{PORT} --upstream-auth {USER}:{PASS} --listen-port 5858'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
atexit.register(p.kill)
while 1:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        if s.connect_ex(('127.0.0.1', 5858)) == 0: break
    sleep(1)


def run_adrino_bot_browser():
    try: page = ChromiumPage(ChromiumOptions().set_argument('--start-maximized').set_argument('--ignore-certificate-errors').auto_port().add_extension('./ProxyExt'))
    except: page = ChromiumPage(ChromiumOptions().set_argument('--start-maximized').set_argument('--ignore-certificate-errors').auto_port().add_extension('./ProxyExt'))
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
        page = page.latest_tab
        page.wait.doc_loaded()
        for x in range(1, 4 + 1):
            sleep(10)
            for i in range(10+1):
                try:
                    ebtn = page.ele('css:#tp-snp2', timeout=10)
                    cookies = json.loads(page.cookies(True).as_json())
                    if x != 4: ebtn.click(by_js=True)
                    else:
                        ref = page.url
                        sLink = ebtn.parent().attr('href')
                    break
                except errors.NoRectError as err:
                    if i == 10: raise err
                    sleep(1)
            sleep(2)
            page.wait.doc_loaded()
        
        oldPage.quit()
        isQuit = True
        s = Session()
        for c in cookies:
            s.cookies.set(**c)
        r = s.get(sLink, headers={'Referer': ref}, allow_redirects=False, stream=True, proxies=dict(http=pr, https=pr))
        loc = r.headers.get('Location')
        if not loc: raise Exception('Error in adrinolinks. No location found.')
        print('Adrino Links:', loc)
    except Exception as err:
        if isQuit: raise err
        else:
            ss = page.get_screenshot(as_bytes=True, full_page=True)
            url = Session().post('https://freeimage.host/api/1/upload', params=dict(key='6d207e02198a847aa98d0a2a901485a5'), files=dict(source=ss)).json().get('image', {}).get('url')
            raise Exception(traceback.format_exc() + '\n\nScreenshot: ' + url)


def run_aro_bot_browser():
    try: page = ChromiumPage(ChromiumOptions().set_argument('--start-maximized').set_argument('--ignore-certificate-errors').auto_port().add_extension('./ProxyExt'))
    except: page = ChromiumPage(ChromiumOptions().set_argument('--start-maximized').set_argument('--ignore-certificate-errors').auto_port().add_extension('./ProxyExt'))
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
        page = page.latest_tab
        page.wait.doc_loaded()
        for _ in range(2):
            scrollAllOver(2)
            try: page.ele('css:#btn7').click(by_js=True)
            except:
                page.ele('css:#tp-snp2').click(by_js=True)
            sleep(2)
            page.wait.doc_loaded()
        
        sleep(2)
        pURL = page.url
        ref = page.run_js('return document.referrer')

        oldPage.quit()
        isQuit = True

        s = Session()
        s.proxies = dict(http=pr, https=pr)
        s.cookies.set('ab', '2', domain='arolinks.com')
        s.get(pURL, headers={'Referer': 'https://hyperapks.xyz/'}, allow_redirects=False, stream=True, timeout=10)
        r = s.get(pURL, headers={'Referer': ref})
        d = BeautifulSoup(r.text, 'html.parser')
        data = { i.get('name') : i.get('value') for i in d.select('#go-link input[name][value]')}
        sleep(int(d.select_one('#timer').text.strip()))
        r = s.post('https://arolinks.com/links/go', headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https:/arolinks.com', 'Referer': pURL}, data=data)
        if 'success' not in r.text: raise Exception('Error in AroLink: %s' % r.text)
        print('AroLink:', r.text)
    except Exception as err:
        if isQuit: raise err
        else:
            ss = page.get_screenshot(as_bytes=True, full_page=True)
            url = Session().post('https://freeimage.host/api/1/upload', params=dict(key='6d207e02198a847aa98d0a2a901485a5'), files=dict(source=ss)).json().get('image', {}).get('url')
            raise Exception(traceback.format_exc() + '\n\nScreenshot: ' + url)


def run_telegramlinks_bot_browser():
    try: page = ChromiumPage(ChromiumOptions().set_argument('--start-maximized').set_argument('--ignore-certificate-errors').auto_port().add_extension('./ProxyExt'))
    except: page = ChromiumPage(ChromiumOptions().set_argument('--start-maximized').set_argument('--ignore-certificate-errors').auto_port().add_extension('./ProxyExt'))
    try:
        oldPage = page
        isQuit = False
        link = random.choice(json.load(open('post_links.json')))
        page.get(f'https://{random.choice(["google.com", "google.com", "facebook.com", "bing.com", "bing.com"])}/robots.txt')
        page.run_js(f"window.location.href='{link}'")
        page.wait.load_start(10, False)
        page.wait.doc_loaded()
        sleep(2)
        def scrollAllOver(speed = 1, background=False):
            if background:
                try:
                    return page.run_async_js('''
                        async function scrollAllOver(speed = 1) {
                            window.scrollTo(0, 0);
                            let currScroll = 0;
                            let totalHeight = document.body.scrollHeight;

                            while (currScroll < totalHeight) {
                                totalHeight = document.body.scrollHeight;
                                const step = (Math.random() * (150 - 50) + 50) * speed;
                                window.scrollBy(0, step);
                                currScroll += step;

                                const delay = (Math.random() * (1.5 - 0.1) + 0.1) * 1000 / speed;
                                await new Promise(resolve => setTimeout(resolve, delay));
                            }
                        }
                        scrollAllOver(%s)
                    ''' % str(speed))
                except: return
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
        sleep(1)
        page.wait.doc_loaded()
        for _ in range(3):
            sleep(3)
            scrollAllOver(background=True)
            page.wait.ele_displayed('css:#btnfianl', 30, True)
            page.ele("css:#btnfianl").click(by_js=True)
        
        sleep(2)
        pURL = page.url
        ref = page.run_js('return document.referrer')
        
        oldPage.quit()
        isQuit = True

        s = Session()
        s.proxies = dict(http=pr, https=pr)
        s.cookies.set('ab', '2', domain='go.telegramlink.in')
        s.get(pURL, headers={'Referer': 'https://hyperapks.xyz/'}, allow_redirects=False, stream=True, timeout=10)
        r = s.get(pURL, headers={'Referer': ref})
        d = BeautifulSoup(r.text, 'html.parser')
        data = { i.get('name') : i.get('value') for i in d.select('#go-link input[name][value]')}
        sleep(int(d.select_one('#timer').text.strip()))
        r = s.post('https://go.telegramlink.in/links/go', headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https:/go.telegramlink.in', 'Referer': pURL}, data=data)
        if 'success' not in r.text: raise Exception('Error in TelegramLink: %s' % r.text)
        print('TelegramLink:', r.text)
    except Exception as err:
        if isQuit: raise err
        else:
            ss = page.get_screenshot(as_bytes=True, full_page=True)
            url = Session().post('https://freeimage.host/api/1/upload', params=dict(key='6d207e02198a847aa98d0a2a901485a5'), files=dict(source=ss)).json().get('image', {}).get('url')
            raise Exception(traceback.format_exc() + '\n\nScreenshot: ' + url)



if __name__ == '__main__':
    run_telegramlinks_bot_browser()

