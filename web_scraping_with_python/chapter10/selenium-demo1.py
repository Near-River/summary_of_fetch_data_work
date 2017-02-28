from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS(executable_path='D:\\phantomjs-2.1.1-windows\\bin\\phantomjs')
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
# time.sleep(3)
# print(driver.find_element_by_id('content').text)
# driver.close()

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'loadedButton'))  # 定位器
    )
finally:
    print(driver.find_element_by_id('content').text)
    print(driver.page_source)
    driver.close()
