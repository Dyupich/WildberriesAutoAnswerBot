import time
import pickle

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


def get_user_number(number: str):
    if isinstance(number, str):
        if len(number) != 10:
            raise TypeError('Неверно набран номер! Длина строки должна быть равна 10')
        return number
    raise TypeError("Неверный тип номера")


def interact_with_element(by, find_string, text="", enter=False, click=False, clear=False):
    button = driver.find_element(by, find_string)
    if click:
        button.click()
    if clear:
        button.clear()
    button.send_keys(text)
    if enter:
        button.send_keys(Keys.ENTER)


if __name__ == '__main__':
    url = 'https://seller.wildberries.ru'
    s = Service('./chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={UserAgent().chrome}")
    driver = webdriver.Chrome(service=s, options=options)

    try:

        driver.get(url)
        time.sleep(2)
        interact_with_element(By.XPATH, "//input", "9250113372", click=True, clear=True, enter=True)

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
