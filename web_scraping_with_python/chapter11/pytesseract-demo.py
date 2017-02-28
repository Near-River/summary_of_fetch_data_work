from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
import subprocess
from PIL import Image, ImageOps


def cleanImage(imagePath):
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x < 143 else 255)
    borderImage = ImageOps.expand(image, border=20, fill='white')
    borderImage.save(imagePath)


html = urlopen('http://www.pythonscraping.com/humans-only')
soup = BeautifulSoup(html, 'html.parser')
# 收集需要处理的表单数据（包括验证码和输入字段）
imageLocation = soup.find('img', {'title': 'Image CAPTCHA'})['src']
formBuildId = soup.find('input', {'name': 'form_build_id'})['value']
captchaSid = soup.find('input', {'name': 'captcha_sid'})['value']
captchaToken = soup.find('input', {'name': 'captcha_token'})['value']

captcha_url = 'http://pythonscraping.com' + imageLocation
urlretrieve(captcha_url, 'captcha.jpg')

cleanImage('captcha.jpg')
p = subprocess.Popen(['tesseract', 'captcha.jpg', 'output'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.wait()
with open('output.txt') as f:
    captchaResponse = f.read().replace(' ', '').replace('\n', '')
print('Captcha solution attempt:', captchaResponse)
