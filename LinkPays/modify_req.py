import os, sys
DIR = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(DIR, '..'))
sys.path.insert(0, parent_dir)

from mitmproxy import http
from proxyscrape import get_session
from mitmproxy.connection import Server
from mitmproxy.net.server_spec import ServerSpec
from func import get_free_port
from time import sleep
import re, subprocess, atexit, socket, requests

while 1:
    try:
        pr = get_session()
        if requests.head('http://linkpays.in/', proxies=dict(http=pr, https=pr)).status_code == 502:
            print('Invalid Status')
            continue
        else: break
    except Exception as err:
        print(err)
        continue

# print(requests.get('http://ip.oxylabs.io', proxies=dict(http=pr, https=pr)).text.strip())
# exit()

USER, PASS, HOST, PORT = re.findall(r'^[^:]+:\/\/([^:]+):([^@]+)@([^:]+):(\d+)$', pr)[0]
proxiedURLs = [
    'google-analytics.com',
    'analytics.google.com',
    'st?api=',
    'safe.php?id=',
    'go.php?id=',
    'links/go',
    re.compile(r"^https?://linkpays\.in/[\w\-]+$"),
]

def write(url):
    lines = []
    try:
        with open('urls.txt') as f: lines = f.readlines()
    except: pass
    lines.append(f'{url}\n')
    with open('urls.txt', 'w') as f:
        f.writelines(lines)


def request(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url
    # write(url)

    # if 'links/go' in url:
    #     flow.request.headers.add('X-Requested-With', 'XMLHttpRequest')

    if url.endswith('.apk') and 'href.li' in flow.request.pretty_host:
        flow.response = http.Response.make(200, b'Prevented it', {'content-type': 'text/plain'})
        return
    
    if isMatch(url):
        flow.server_conn = Server(address=flow.server_conn.address)
        flow.server_conn.via = ServerSpec(('http', (HOST, PORT)))
        return


def isMatch(url):
    for u in proxiedURLs:
        if type(u) == re.Pattern:
            if u.findall(url):
                return True
        else:
            if u in url:
                return True
    return False


def runProxyServer(wait=False):
    PORT = get_free_port()
    p = subprocess.Popen(f'mitmdump -s {__file__} --listen-port {PORT} --upstream-auth {USER}:{PASS}'.split(),
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL
                        )
    atexit.register(p.kill)

    while 1:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            if s.connect_ex(('127.0.0.1', PORT)) == 0: break
        sleep(1)

    if wait:
        print('ProxyServer is running on port', PORT)
        p.wait()
    else:
        return PORT

if __name__ == '__main__':
    runProxyServer(1)

