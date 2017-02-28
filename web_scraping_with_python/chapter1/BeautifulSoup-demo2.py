import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Demo1:
html = urlopen(url='http://www.pythonscraping.com/pages/warandpeace.html')
bsObj = BeautifulSoup(html.read(), 'html.parser')

nameList = bsObj.findAll('span', {'class': 'green'})
for elem in nameList:
    print(elem)

# Demo2:
html = urlopen(url='http://www.pythonscraping.com/pages/page3.html')
bsObj = BeautifulSoup(html.read(), 'html.parser')

images = bsObj.findAll('img', {'src': re.compile(r'../img/gifts/img.*.jpg')})
for img in images:
    print(img['src'])

tags = bsObj.findAll(lambda tag: len(tag.attrs) == 2)
print(len(tags))
