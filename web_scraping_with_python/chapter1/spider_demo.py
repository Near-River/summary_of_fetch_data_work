from urllib import request


html = request.urlopen('http://iir.circ.gov.cn/web/nametoinfo!toinfo.html?peopleId=12345678')
# print(html.read())
html_txt = html.read().decode(encoding='utf-8', errors='ignore')
print(html_txt)