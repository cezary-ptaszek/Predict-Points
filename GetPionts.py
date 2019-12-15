import requests
import re
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup


url = 'https://stackoverflow.com/questions/tagged/java?tab=newest&page=107917&pagesize=15'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

tab = []

for text in soup.find_all('a'):
    temp = text.get('href')
    if isinstance(temp, str):
        if re.match(r'^\/questions\/\d+\/.*',temp):
            tab.append(temp)

print(tab)

    # links = re.match(^\/questions\/\d+\/.*)


# base = 'https://stackoverflow.com'
# for i, link in enumerate(links):
#     if not urlparse(link).netloc:
#         link_with_base = base + '/' + link
#         links[i] = link_with_base