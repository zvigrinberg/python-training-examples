# https://www.google.com/search?q=what+is+CVE-2024-41270
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,"
                         " like Gecko) Chrome/128.0.0.0 Safari/537.36"}
URL = "https://www.google.com/search?q=what+is+CVE-2024-41270"
r = requests.get(url=URL, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
result = soup.find('div', attrs={'id': 'search'}).find('b').parent.text


print(result)
