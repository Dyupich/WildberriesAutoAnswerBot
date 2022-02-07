import time
import pickle

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


if __name__ == '__main__':
    url = 'https://seller.wildberries.ru/feedback-question/feedbacks/not-answered-feedbacks'
    s = Service('./chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={UserAgent().chrome}")
    driver = webdriver.Chrome(service=s, options=options)

    try:
        driver.get(url)
        time.sleep(5)
        driver.delete_all_cookies()
        for cookie in pickle.load(open(f"9250113372_cookies", "rb")):
            print(cookie)
            driver.add_cookie(cookie)
        driver.refresh()

        check = input("Если вы успешно авторизовались, введите 'yes', в ином случае введите 'no'\n>>>")
        if check == "yes":
            pickle.dump(driver.get_cookies(), open('9250113372_cookies', 'wb'))
        else:
            print("Данные о входе не сохранены. Вам необходимо перезапустить приложение для входа.")
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()