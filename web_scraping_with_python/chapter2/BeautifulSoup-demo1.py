from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import datetime
import re

random.seed(datetime.datetime.now())  # create a random generator


def getLinks(articleUrl):
    response = urlopen(url='http://en.wikipedia.org' + articleUrl)
    bsObj = BeautifulSoup(response.read(), 'html.parser')
    return bsObj.find('div', {'id': 'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))


links = getLinks(articleUrl='/wiki/Kevin_Bacon')
while len(links) > 0:
    newArticle = links[random.randint(0, len(links) - 1)].attrs['href']
    print(newArticle)
    links = getLinks(newArticle)
