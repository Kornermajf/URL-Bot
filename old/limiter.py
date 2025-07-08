import requests as r
import inspect

class CurrentDate:
    d = None
    @property
    def current(s):
        if not s.d: s.d = get_date()
        return s.d


date = CurrentDate()

def get_date():
    x = r.get('https://timeapi.io/api/timezone/zone?timeZone=Asia/Dhaka')
    dt = x.json().get('currentLocalTime', 'idk9910').split('T')[0]
    return dt

def isCompleted(t:int, idn:str):
    c = getRecord(idn)
    return True if c >= t else False


def submitOne(idn: str):
    q = r.get(f'https://letscountapi.com/{idn}/{date.current}')
    if not q.json()['exists']:
        r.post(f'https://letscountapi.com/{idn}/{date.current}', data='{"current_value": 0}', headers={'Content-Type': 'application/json'})
    w = r.post(f'https://letscountapi.com/{idn}/{date.current}/increment')
    c = int(w.json().get('current_value', 0))
    return c


def getRecord(idn: str):
    q = r.get(f'https://letscountapi.com/{idn}/{date.current}')
    c = int(q.json().get('current_value', 0))
    return c

if __name__ == '__main__':
    print(getRecord('urlbot-arolink'))
