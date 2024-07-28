import requests as r
import inspect


def get_date():
    x = r.get('https://worldtimeapi.org/api/timezone/Asia/Dhaka')
    dt = x.json().get('datetime', 'idk9910').split('T')[0]
    return dt

cur_date = get_date()

def isCompleted(t:int, idn:str):
    c = getRecord(idn)
    return True if c >= t else False

def submitOne(idn:str):
    q = r.get(f'https://api.counterapi.dev/v1/{idn}/{cur_date}/up')
    c = int(q.json().get('count', 0))
    return c

def getRecord(idn:str):
    q = r.get(f'https://api.counterapi.dev/v1/{idn}/{cur_date}')
    c = int(q.json().get('count', 0))
    return c

