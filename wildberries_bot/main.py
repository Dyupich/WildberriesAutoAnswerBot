# -*- coding: utf-8 -*-
import pickle
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
        # open url
        controller.driver.get('https://seller.wildberries.ru/feedback-question/feedbacks/not-answered-feedbacks')
        # remove cookies
        controller.driver.delete_all_cookies()
        print("[INFO] Cookies deleted")
        # add cookies of saved user
        for cookie in pickle.load(open(f"{user_number}_cookies", "rb")):
            # print(cookie)
            controller.driver.add_cookie(cookie)
        print(f"[INFO] cookies for +7{user_number} loaded")
        # restarting our page
        controller.driver.refresh()
        print("[INFO] Page is refreshed")
        # changing reviews list from 5_items to 100_items
        controller.make_100_reviews_at_page()
        print("[INFO] Controller.make_100_reviews_at_page method is done")
        # main loop
        controller.answer_on_reviews()
        input("Введите что-либо для завершения\n>>>")
    except FileNotFoundError as ex:
        print("Вы указали данные пользователя, чьи данные для входа еще не были сохранены.")
    except Exception as ex:
        with open("exception_log.log", "w") as f:
            f.write(repr(ex))
        print(repr(ex))
        print("[ERROR] Check exception message here or in exception_log.log")
        input("Введите что-либо для завершения\n>>>")
    finally:
        controller.driver.close()
        controller.driver.quit()
