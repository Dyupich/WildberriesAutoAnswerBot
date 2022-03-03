# -*- coding: utf-8 -*-
import pickle
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from TemplateCreator import create_template


def set_last_user(user_number: str):
    with open("last_user.txt", "w") as file:
        file.write(user_number)


def get_last_user():
    with open("last_user.txt", "r") as file:
        return file.read()


def is_correct_number(number: str):
    if isinstance(number, str):
        if len(number) != 10 or not number.isdigit():
            return False
        return True
    return False


if __name__ == '__main__':
    print("Программа, отвечающая на отзывы Wildberries по шаблону.\n"
          "------------------------------------------------------------------\n"
          )

    menu = int(input("Введите число из меню ниже: \n"
                     f"1 - Вход по номеру последнего пользователя ({get_last_user()}).\n"
                     f"2 - Вход по другому номеру.\n"
                     f">>>"))
    user_number = ""
    if menu == 1:
        user_number = get_last_user()
    elif menu == 2:
        while not is_correct_number(user_number):
            user_number = input(
                "Введите номер пользователя для входа в аккаунт Wildberries.\n"
                "Формат номера: 92223334455\n"
                "При неверном наборе вы вернетесь на этот шаг снова.\n"
                ">>>")

        set_last_user(user_number)
    try:
        url = 'https://seller.wildberries.ru/feedback-question/feedbacks/not-answered-feedbacks'
        s = Service('./chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={UserAgent().chrome}")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=s, options=options)
        driver.get(url)
        driver.delete_all_cookies()
        for cookie in pickle.load(open(f"{user_number}_cookies", "rb")):
            # print(cookie)
            driver.add_cookie(cookie)
        driver.refresh()
        reviews = []
        while len(reviews) == 0:
            reviews = driver.find_elements(By.XPATH, r'//ul[@class="feedbackCardsList"]'
                                                     r'/li')

        page = 2
        while int(driver.find_element(By.XPATH, r'//li[contains(@class, "pageTabsItem")][1]'
                                                r'/*/span[contains(@class, "tabCount")]'
                                                r'/span').text) > 0:
            while len(reviews) == 0:
                reviews = driver.find_elements(By.XPATH, r'//ul[@class="feedbackCardsList"]'
                                                         r'/li')

            for i in range(len(reviews)):
                if len(driver.find_elements(By.XPATH, r'//ul[@class="feedbackCardsList"]'
                                                      f'/li[{i + 1}]//div[@class="classContentInfo"]'
                                                      r'//div[contains(@class, "one")]')) == 5:

                    if len(driver.find_elements(By.XPATH, '//span[text()="Принимаю"]')) > 0:
                        driver.find_element(By.XPATH, '//span[text()="Принимаю"]').click()
                    answer = driver.find_element(By.XPATH, f'//ul[@class="feedbackCardsList"]'
                                                           f'//li[{i + 1}]'
                                                           f'//*[text()="Ответ"]')
                    answer.click()

                    answer_field = driver.find_element(By.XPATH, f'//ul[@class="feedbackCardsList"]'
                                                                 f'//li[{i + 1}]'
                                                                 f'//div[@class="Text-area-input"]'
                                                                 f'//*')

                    product_code = driver.find_element(By.XPATH, '//ul[@class="feedbackCardsList"]'
                                                                 f'//li[{i + 1}]'
                                                                 '//*[text()="Артикул поставщика"]'
                                                                 '/../..//*[2]'
                                                       ).text

                    txt = create_template("Шаблон.xlsx", product_code=product_code)
                    if txt[:6] == "Ошибка":
                        continue
                    answer_field.send_keys(txt)

                    print(f"Отзыв {i + 1} имеет следующий ответ:\n{txt}\n")

                    time.sleep(1.5)
                    answer_button = driver.find_element(By.XPATH, f'//ul[@class="feedbackCardsList"]'
                                                                  f'/li[{i + 1}]//'
                                                                  f'span[text()="Ответить"]')
                    answer_button.click()
                    time.sleep(1)

            if len(driver.find_elements(By.XPATH,
                                        r'//div[contains(@class, "paginationButtonsContainer")]'
                                        r'/*/div[contains(@class, "paginationBoxViewDesktop")]'
                                        f'/*//span[text()="{page}"]')) == 1:
                button = driver.find_element(By.XPATH,
                                             r'//div[contains(@class, "paginationButtonsContainer")]'
                                             r'/*/div[contains(@class, "paginationBoxViewDesktop")]'
                                             f'/*//span[text()="{page}"]')
                button.click()
                page += 1
                driver.execute_script('scroll(0, -500)')
                time.sleep(2)
            else:
                break

        check = input("Введите что-либо для завершения\n>>>")
    except FileNotFoundError as ex:
        print("Вы указали данные пользователя, чьи данные для входа еще не были сохранены.")
    except Exception as ex:
        print(ex)
        raise ex
    finally:
        driver.close()
        driver.quit()
