from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

# Version 1:
response = urlopen(url='http://www.pythonscraping.com/pages/page1.html')
bsObj = BeautifulSoup(response.read(), 'html.parser')
print(bsObj.h1)


# Version 2:
def getTitle(url):
    try:
        html = urlopen(url=url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title


title = getTitle(url='http://www.pythonscraping.com/pages/page1.html')
if title is None:
    print('Title could not be found')
else:
    print(title)
