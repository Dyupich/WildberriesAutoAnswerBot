# -*- coding: utf-8 -*-
import pickle

from main import is_correct_number
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

if __name__ == '__main__':
    user_number = ""
    print("Приложение для сохранения данных сессии пользователя в Wildberries.\n"
          "------------------------------------------------------------------\n")
    while not is_correct_number(user_number):
        user_number = input(
            "Введите номер пользователя для входа в аккаунт Wildberries.\n"
            "Формат номера: 92223334455\n"
            "При неверном наборе вы вернетесь на этот шаг снова.\n"
            ">>>")

    try:
        url = 'https://seller.wildberries.ru'
        s = Service('./chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={UserAgent().chrome}")
        driver = webdriver.Chrome(service=s, options=options)
        driver.get(url)

        while len(driver.find_elements(By.XPATH, "//input")) == 0:
            pass

        input_button = driver.find_element(By.XPATH, "//input")
        input_button.click()
        input_button.clear()
        input_button.send_keys(user_number)
        input_button.send_keys(Keys.ENTER)

        check = input("Если вы успешно авторизовались, введите 'yes', в ином случае введите 'no'.\n>>>")

        if check == "yes":
            pickle.dump(driver.get_cookies(), open(f'{user_number}_cookies', 'wb'))
        else:
            print("Данные о входе не сохранены. Вам необходимо перезапустить приложение для входа.")
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
