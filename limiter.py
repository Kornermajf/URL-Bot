import requests as r
import inspect


def get_date():
    x = r.get('https://timeapi.io/api/timezone/zone?timeZone=Asia/Dhaka')
    dt = x.json().get('currentLocalTime', 'idk9910').split('T')[0]
    return dt

cur_date = get_date()

def isCompleted(t:int, idn:str):
    c = getRecord(idn)
    return True if c >= t else False


def submitOne(idn: str):
    q = r.get(f'https://letscountapi.com/{idn}/{cur_date}')
    if not q.json()['exists']:
        r.post(f'https://letscountapi.com/{idn}/{cur_date}', data='{"current_value": 0}', headers={'Content-Type': 'application/json'})
    w = r.post(f'https://letscountapi.com/{idn}/{cur_date}/increment')
    c = int(w.json().get('current_value', 0))
    return c


def getRecord(idn: str):
    q = r.get(f'https://letscountapi.com/{idn}/{cur_date}')
    c = int(q.json().get('current_value', 0))
    return c

