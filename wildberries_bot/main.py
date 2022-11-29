# -*- coding: utf-8 -*-
import pickle
import time
from Controller import Controller


def is_correct_number(number: str):
    if isinstance(number, str):
        if len(number) != 10 or not number.isdigit():
            return False
        return True
    return False


def menu():
    def set_last_user(user_number: str):
        with open("last_user.txt", "w") as file:
            file.write(user_number)

    def get_last_user():
        with open("last_user.txt", "r") as file:
            return file.read()

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
    return user_number


if __name__ == '__main__':
    user_number = menu()
    try:
        controller = Controller()
        controller.driver.get('https://seller.wildberries.ru/feedback-question/feedbacks/not-answered-feedbacks')
        # open url
        # remove cookies
        controller.driver.delete_all_cookies()
        # add cookies of saved user
        for cookie in pickle.load(open(f"{user_number}_cookies", "rb")):
            # print(cookie)
            controller.driver.add_cookie(cookie)
        # restarting our page
        controller.driver.refresh()
        # changing reviews list from 5_items to 100_items
        controller.make_100_reviews_at_page()

        # main loop
        controller.answer_on_reviews()
        # reviews = []
        # while len(reviews) == 0:
        #     reviews = driver.find_elements(By.XPATH, r'//ul[@class="feedbackCardsList"]/li')
        # answer = []
        # page = 1
        # check_accept()
        # while int(driver.find_element(By.XPATH, r'//li[contains(@class, "pageTabsItem")][1]'
        #                                         r'/*/span[contains(@class, "tabCount")]'
        #                                         r'/span').text) > 0:
        #     while len(reviews) == 0:
        #         reviews = driver.find_elements(By.XPATH, r'//ul[@class="feedbackCardsList"]'
        #                                                  r'/li')
        #     check_accept()
        #     for i in range(len(reviews)):
        #         if len(driver.find_elements(By.XPATH, r'//ul[@class="feedbackCardsList"]'
        #                                               f'/li[{i + 1}]//div[@class="classContentInfo"]'
        #                                               r'//div[contains(@class, "one")]')) == 5:
        #
        #             check_accept()
        #             if page > 2 and type(answer) != list:
        #                 while answer == driver.find_element(By.XPATH, f'//ul[@class="feedbackCardsList"]'
        #                                                               f'//li[{i + 1}]'
        #                                                               f'//*[text()="Ответ"]'):
        #                     driver.execute_script('scroll(0, -800)')
        #                     time.sleep(3)
        #
        #             answer = driver.find_element(By.XPATH, f'//ul[@class="feedbackCardsList"]'
        #                                                    f'//li[{i + 1}]'
        #                                                    f'//*[text()="Ответ"]')
        #             answer.click()
        #
        #             answer_field = driver.find_element(By.XPATH, f'//ul[@class="feedbackCardsList"]'
        #                                                          f'//li[{i + 1}]'
        #                                                          f'//div[@class="Text-area-input"]'
        #                                                          f'//*')
        #
        #             product_code = driver.find_element(By.XPATH, '//ul[@class="feedbackCardsList"]'
        #                                                          f'//li[{i + 1}]'
        #                                                          '//*[text()="Артикул поставщика"]'
        #                                                          '/../..//*[2]'
        #                                                ).text
        #
        #             txt = create_template("Шаблон.xlsx", product_code=product_code)
        #             if txt[:6] == "Ошибка":
        #                 print(txt)
        #                 continue
        #             check_accept()
        #             answer_field.send_keys(txt)
        #
        #             print(f"Отзыв {i + 1} имеет следующий ответ:\n{txt}\n")
        #
        #             answer_button = driver.find_element(By.XPATH, f'//ul[@class="feedbackCardsList"]'
        #                                                           f'/li[{i + 1}]//'
        #                                                           f'span[text()="Ответить"]')
        #             check_accept()
        #             answer_button.click()
        #             while answer_button.text != "Ответ отправлен":
        #                 pass
        #
        #     if len(driver.find_elements(By.XPATH,
        #                                 r'//button[contains(@class, "iconButton")]'
        #                                 r'//*[contains(@class, "backwards")]')) == 1:
        #         button = driver.find_element(By.XPATH,
        #                                      '//button[contains(@class, "iconButton")]//*[contains(@class, "backwards")]')
        #         button.click()
        #         driver.execute_script('scroll(0, -800)')
        #         time.sleep(3)
        #         page += 1
        #         print(f'Бот нажал стрелку {page} раз')
        #     else:
        #         break

        check = input("Введите что-либо для завершения\n>>>")
    except FileNotFoundError as ex:
        print("Вы указали данные пользователя, чьи данные для входа еще не были сохранены.")
    except Exception as ex:
        print(ex)
        raise ex
    finally:
        controller.driver.close()
        controller.driver.quit()
