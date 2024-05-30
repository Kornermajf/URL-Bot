from seleniumwire import webdriver
from time import sleep


def request_interceptor(request):
    if request.host.__contains__('google-analytics.com') and request.method.upper() == 'POST':
        url, headers = request.url, request.headers
        print(url)


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-logging')
options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=options)
driver.request_interceptor = request_interceptor

driver.get('https://www.flixwonders.com')


sleep(10)
driver.quit()

