from cloudscraper import CloudScraper as Session
# from all_links import *
# from telegramlinks import run_telegram_bot
# from arolinks import run_arolink_bot
# from teraboxlinks import run_tera_bot_browser
# from browser_bot import run_telegramlinks_bot_browser
# from nanolinks import run_nano_bot
# from nanolinks import run_nano_bot_browser
# from onylinks import run_ony_bot_browser
# from adrinolinks import run_adrino_bot
# from kingurl import run_kingurl_bot
# from udlinks import run_udlinks_bot
# from malink import run_malink_bot
# from zagl import run_zagl_bot
from random import randint
import urllib3, threading, sys, subprocess, os
from time import sleep
Thread=threading.Thread

d={'e':''}

def excepthook(l):
    d['e']+=str(l.exc_value) + '\n\n'

threading.excepthook=excepthook

def main(proxy=None, **kw):
    t=[]
    # subprocess.Popen(f'{sys.executable} {os.path.join('ShareDiskLink', 'sdl_bot.py')}'.split()).wait()
    # t.append(Thread(target=lambda: run_terabox_bot(random_teraboxlinks, proxy, **kw)))
    # t.append(Thread(target=lambda: run_nano_bot(random_nanolinks, proxy, **kw)))
    # t.append(Thread(target=run_telegramlinks_bot_browser))
    # t.append(Thread(target=lambda: run_arolink_bot(proxy, **kw)))
    # t.append(Thread(target=lambda: run_adrino_bot(random_adrino, proxy, **kw)))
    # t.append(Thread(target=lambda: run_udlinks_bot(random_udlinks, proxy, **kw)))
    # t.append(Thread(target=lambda: run_malink_bot(random_malink, proxy, **kw)))


    for v in t: v.start()
    for v in t: v.join()
    
    if d['e']!='': raise Exception(d['e'])
    # Slow earning speed
    sleep(300)



if __name__ == '__main__':
    main()
