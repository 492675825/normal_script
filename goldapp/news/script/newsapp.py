from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  #等待页面加载
from selenium.webdriver.common.by import By
import time


class get_page:
    def __init__(self):
        pass

    def get_data(self):

        driver = webdriver.Chrome()
        driver.get("http://www.xinhuanet.com/fortunepro/yanbao/index.html")
        # driver.find_element(By.CLASS_NAME, 'xpage-more-btn')
        while True:
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'xpage-more-btn').click()



if __name__ == '__main__':
    data = get_page()
    data.get_data()
