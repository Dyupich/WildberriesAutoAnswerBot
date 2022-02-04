import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

if __name__ == '__main__':
    url = 'https://seller.wildberries.ru'
    s = Service('./chromedriver.exe')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=s)
    del s

    try:
        driver.get(url)
        time.sleep(10)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
