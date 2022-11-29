import pandas

from random import randint


def create_template(file_name: str, product_code=""):
    if isinstance(file_name, str):
        # reading page with templates
        df = pandas.read_excel("Шаблон.xlsx", sheet_name='ШаблонОтвета')

        # make some field for answers
        start = df.values[randint(0, df.shape[0] - 1)][0]
        gratitude = df.values[randint(0, df.shape[0] - 1)][1]
        main_text = df.values[randint(0, df.shape[0] - 1)][2]

        df = pandas.read_excel("Шаблон.xlsx", sheet_name='Идентификаторы')
        returning_txt = f"Ошибка! Артикул товара, который привел к ошибке {product_code}"
        category = ""
        company = ""
        for i in range(0, df.shape[0]):
            if df.values[i][2] == product_code:
                company = df.values[i][0]
                category = df.values[i][1]
                break
        if category == "" or company == "":
            return returning_txt
        df = pandas.read_excel("Шаблон.xlsx", sheet_name='Ключевики')
        finded = False
        key = ""
        for i in range(0, df.shape[1]):
            if df.columns[i] == category:
                finded = True
                key = df.values[randint(0, df.shape[0] - 1)][i]
        if not finded:
            return f"Ошибка! Категория {category} не была найдена в файле Шаблон.xlsx!"
        df = pandas.read_excel("Шаблон.xlsx", sheet_name='ОкончаниеОтвета')
        end = " " + df.values[randint(0, df.shape[0] - 1)][0] + company

        return start + gratitude + main_text + key + end
    raise TypeError("Параметр 'file_name' должен быть экземлпяром класса 'str'.")


if __name__ == '__main__':
    txt = create_template(file_name="Шаблон.xlsx", product_code='SI1005')
    print(txt)
