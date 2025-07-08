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
import re, subprocess, atexit, socket

pr = get_session()
USER, PASS, HOST, PORT = re.findall(r'^[^:]+:\/\/([^:]+):([^@]+)@([^:]+):(\d+)$', pr)[0]
proxiedURLs = [
    'google-analytics.com',
    'analytics.google.com',
    'sharedisklinks.com',
    '/safe.php',
    '/open.php',
    'over_proxy'
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
    # write(flow.request.pretty_url)
    if flow.request.pretty_url.endswith('.apk') and flow.request.pretty_host == 'href.li':
        flow.response = http.Response.make(200, b'Prevented it', {'content-type': 'text/plain'})
        return
    
    if True in [i in flow.request.pretty_url for i in proxiedURLs]:
        flow.server_conn = Server(address=flow.server_conn.address)
        flow.server_conn.via = ServerSpec(('http', (HOST, PORT)))
        return


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

