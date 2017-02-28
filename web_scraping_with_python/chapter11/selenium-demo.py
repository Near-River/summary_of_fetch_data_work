import time
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path='D:\\phantomjs-2.1.1-windows\\bin\\phantomjs')
# driver = webdriver.Firefox(executable_path='C:\\Program Files\\Mozilla Firefox\\firefox')
driver.get('http://www.amazon.com/War-Peace-Leo-Nidolayevich-Tolstoy/dp/1427030200')
time.sleep(2)

print(driver.page_source)
driver.quit()
# exit()

# 单击图书预览按钮
driver.find_element_by_id('sitbLogoImg').click()
imageList = set()

# 等待页面加载完成
time.sleep(5)
# 当向右箭头可以点击时，开始翻页
while 'pointer' in driver.find_element_by_id('sitbReaderRightPageTurner').get_attribute('style'):
    driver.find_element_by_id('sitbReaderRightPageTurner').click()
    time.sleep(2)
    # 获取已加载页面
    pages = driver.find_elements_by_xpath("//div[@class='pageImage']/div/img")
    for page in pages:
        image = page.get_attribute('src')
        imageList.add(image)

driver.quit()
