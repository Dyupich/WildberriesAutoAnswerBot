import pandas

from random import randint


def create_template(file_name: str, product_code=""):
    if isinstance(file_name, str):
        df = pandas.read_excel("Шаблон.xlsx", sheet_name='ШаблонОтвета')
        start = df.values[randint(0, df.shape[0] - 1)][0]
        gratitude = df.values[randint(0, df.shape[0] - 1)][1]
        main_text = df.values[randint(0, df.shape[0] - 1)][2]

        df = pandas.read_excel("Шаблон.xlsx", sheet_name='Идентификаторы')
        category = ""
        company = ""
        for i in range(0, df.shape[0]):
            if df.values[i][2] == product_code:
                company = df.values[i][0]
                category = df.values[i][1]
                break
        df = pandas.read_excel("Шаблон.xlsx", sheet_name='Ключевики')
        finded = False
        key = ""
        for i in range(0, df.shape[1]):
            if df.columns[i] == category:
                finded = True
                key = df.values[randint(0, df.shape[0] - 1)][i]
        if not finded:
            # raise Exception(f"Категория {category} не была найдена в файле Шаблон.xlsx!")
            print(f"Категория {category} не была найдена в файле Шаблон.xlsx!")
        df = pandas.read_excel("Шаблон.xlsx", sheet_name='ОкончаниеОтвета')
        end = df.values[randint(0, df.shape[0] - 1)][0] + company

        return start + gratitude + main_text + key + end
    raise TypeError("Параметр 'file_name' должен быть экземлпяром класса 'str'.")


if __name__ == '__main__':
    print(create_template(file_name="Шаблон.xlsx", product_code='HD-1000.'))
