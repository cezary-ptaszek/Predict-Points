import requests
import re
from bs4 import BeautifulSoup
import time
from array import *


def open_link(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.text, "html.parser")

links = []
upvotes = []

url = 'https://stackoverflow.com/questions/tagged/java?tab=newest&page=107917&pagesize=15'

for text in open_link(url).find_all('a'):
    temp = text.get('href')
    if isinstance(temp, str):
        if re.match(r'^\/questions\/\d+\/.*',temp):
            links.append('https://stackoverflow.com' + temp)

# print(links)

# pierwsze 4 odpowiedzi
for t in links:
    soup = open_link(t)
    print(t)
    i = 0
    for text in soup.find_all('div'):
        temp = text.get('data-value')
        if i > 1 and isinstance(temp, str):
            upvotes.append(temp)
        if i==6:
            break
        if isinstance(temp, str):
            i+=1
    time.sleep(1)

print(upvotes)


