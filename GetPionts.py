import requests
import re
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

RANGE = 100
NUMERPERPAGE = 50

def open_link(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.text, "html.parser")


# liczba w tablicy
upvotes = []
upvotesTest = []
numOfChars = []
numOfCharsTest = []
z = 0

f = open("log.txt", "a")

number = 20499
for i in range(RANGE):
    links = []
    url = 'https://stackoverflow.com/questions/tagged/java?tab=newest&page=' + str(number) + '&pagesize=' + str(NUMERPERPAGE)

    for text in open_link(url).find_all('a'):
        temp = text.get('href')
        if isinstance(temp, str):
            if re.match(r'^\/questions\/\d+\/.*', temp):
                links.append('https://stackoverflow.com' + temp)

    # pierwsza odpowiedz
    for t in links:
        soup = open_link(t)
        print(t)
        f.write(t + '\n')
        k = 0
        for text in soup.find_all('div'):
            temp = text.get('data-value')
            if k > 1 and isinstance(temp, str):
                upvotes.append(int(temp))
            if k == 3:
                break
            if isinstance(temp, str):
                k += 1

        for hit in soup.findAll(attrs={'class': 'answercell post-layout--right'}):
            hit = hit.text.strip()
            numOfChars.append(len(hit.split()))
            break
        z += 1

        time.sleep(1)

    print(upvotes)
    print(numOfChars)
    f.write(str(upvotes) + '\n')
    f.write(str(numOfChars) + '\n')
    number += 1

number = 10499

for i in range(50):
    links = []
    url = 'https://stackoverflow.com/questions/tagged/java?tab=newest&page=' + str(number) + '&pagesize=' + str(NUMERPERPAGE)

    for text in open_link(url).find_all('a'):
        temp = text.get('href')
        if isinstance(temp, str):
            if re.match(r'^\/questions\/\d+\/.*', temp):
                links.append('https://stackoverflow.com' + temp)

    # pierwsza odpowiedz
    for t in links:
        soup = open_link(t)
        print(t)
        f.write(t + '\n')
        k = 0
        for text in soup.find_all('div'):
            temp = text.get('data-value')
            if k > 1 and isinstance(temp, str):
                upvotesTest.append(int(temp))
            if k == 3:
                break
            if isinstance(temp, str):
                k += 1

        for hit in soup.findAll(attrs={'class': 'answercell post-layout--right'}):
            hit = hit.text.strip()
            numOfCharsTest.append(len(hit.split()))
            break
        z += 1
        time.sleep(1)

    print(upvotesTest)
    print(numOfCharsTest)
    f.write(str(upvotesTest) + '\n')
    f.write(str(numOfCharsTest) + '\n')
    number += 1

diff = len(upvotes) - len(upvotesTest)
diff1 = abs(diff)
if diff > 0:
    for i in range(diff):
        upvotesTest.append(0)
        numOfCharsTest.append(0)
elif diff == 0:
    print("Tablice równe")
    f.write("Tablice równe")
else:
    for i in range(diff1):
        upvotes.append(0)
        numOfChars.append(0)

# Regresja
regr = linear_model.LinearRegression()
numOfChars2d = np.reshape(numOfChars, (-1, 1))
upvotes2d = np.reshape(upvotes, (-1, 1))
regr.fit(numOfChars2d, upvotes2d)
numOfCharsTest2d = np.reshape(numOfCharsTest, (-1, 1))
upvotesTest2d = np.reshape(upvotesTest, (-1, 1))
upvotesPred = regr.predict(numOfCharsTest2d)
print('Coefficients: \n', regr.coef_)
# f.write('Coefficients: \n', regr.coef_)
# The mean squared error
print('Mean squared error: %.2f' % mean_squared_error(upvotesTest2d, upvotesPred))
# f.write('Mean squared error: %.2f' % mean_squared_error(upvotesTest2d, upvotesPred))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f' % r2_score(upvotesPred, upvotesTest2d))
# f.write('Coefficient of determination: %.2f' % r2_score(upvotesPred, upvotesTest2d))

f.close()

# Wykresy
gs = gridspec.GridSpec(2, 2)
plt.figure()

plt.subplot(gs[0, 0])
upvotes.sort()
print(upvotes)
plt.hist(upvotes, bins=100)
plt.title("Częstotliwość ocen")

plt.subplot(gs[0, 1])
plt.plot(numOfChars, upvotes, 'bo')
plt.grid(True)
plt.title("Wykres")#

plt.subplot(gs[1, :])
plt.scatter(numOfChars, numOfCharsTest,  color='black')
plt.plot(upvotesTest, upvotesPred, color='blue', linewidth=3)
plt.xticks(())
plt.yticks(())

plt.show()