from requests import get
from random import choices, randint, choice
from string import ascii_letters, digits
import requests, random, os

def get_session():
    pr = os.environ.get('PROXY_URL')
    if not pr: raise Exception('Set Environ Variable first!')
    pr = requests.get(pr).text.strip()
    countries = ['us', 'gb', 'au', 'ca', 'in', 'mx', 'nz']
    country = choice(countries)
    st = ''.join(choices(digits, k=randint(8,20)))
    pr = pr.replace('{COUNTRY}', country).replace('{SESSION}', st).replace('{TIME}', '10')
    return pr

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


if __name__ == '__main__':
    pr = get_session()
    print(pr)
    r=get('https://ip.oxylabs.io', proxies={'http':pr,'https':pr})
    print(r.text)
    
    
    