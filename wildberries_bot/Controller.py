import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from TemplateCreator import create_template

XPathes = {
    "accept_cookie": r'//span[text()="Принимаю"]',
    "show_notes_button": r'//div[contains(@class, "Pagination__select-container")]',
    "choose_100_items": r'//div[contains(@class, "Pagination__select-container")]'
                        r'//*[contains(text(), 100)]',
    "reviews": r'//li[@class="FeedbacksCardsView__list-item"]',
    "review_counter": r'(//span[contains(@class, "Tab--page__count")]//span[@data-name="Counter"])[1]',
    "arrow_to_next_page": r'//button[contains(@class, "Pagination-icon-button")]//*[name()="path" and contains(@d, "M7.58586")]/../..',
    "star_list": r'//li[contains(@class, "Rating-stars-list")]',
    "active_star": r'//span[@style="width: 16px;"]',
    "vendor_code": r'//span[text()="Артикул поставщика"]/../../span[contains(@class, "Text")]',
    "circle_icons": r'//span[contains(@class, "CircleIcon")]/..',
    "text_area": r'//textarea',
    "answer": r'//span[text()="Ответить"]'
}


class Controller:
    def __init__(self):
        s = Service('./chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={UserAgent().chrome}")
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=s, options=options)

    def __check_creation(self, xpath: str) -> None:
        while len(self.driver.find_elements(By.XPATH, xpath)) == 0:
            time.sleep(5)

    def click_on_item_xpath(self, xpath: str) -> None:
        """
        This method clicks on element by Xpath after checking creation
        :param xpath -> xpath to the web element (Example: //div[@class="review"])
        """
        self.__check_creation(xpath)
        self.driver.find_element(By.XPATH, xpath).click()

    def make_100_reviews_at_page(self) -> None:
        """This method reformat page to contain 100 reviews"""
        for xpath in ["accept_cookie", "show_notes_button", "choose_100_items"]:
            self.click_on_item_xpath(XPathes[xpath])

    def get_reviews_counter(self) -> int:
        """This method returns counter of current reviews from Wildberries personal account"""
        self.__check_creation(XPathes["review_counter"])
        return int(self.driver.find_element(By.XPATH, XPathes["review_counter"]).text[:2])

    def get_reviews(self) -> list:
        """This method return list of WebElements (reviews from page)"""
        self.__check_creation(XPathes["reviews"])
        while len(self.driver.find_elements(By.XPATH, XPathes["reviews"])) == 5 \
                and self.get_reviews_counter() != 5:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
        return self.driver.find_elements(By.XPATH, XPathes["reviews"])

    def answer_on_reviews(self) -> None:
        # Actual method for 29.11.2022

        # Exit trigger
        if self.get_reviews_counter() == 0:
            return
        self.driver.execute_script("window.scrollTo(0, 0);")
        reviews = self.get_reviews()

        for i, review in enumerate(reviews):
            # Set review to the bottom of screen
            self.driver.execute_script("arguments[0].scrollIntoView(false);", review)

            # Unique XPathes for reviews
            review_xpath = f'{XPathes["reviews"]}[{i + 1}]'
            star_list_xpath = f'{review_xpath}{XPathes["star_list"]}{XPathes["active_star"]}'
            vendor_code_xpath = f'{review_xpath}{XPathes["vendor_code"]}'
            circle_icons_xpath = f'{review_xpath}{XPathes["circle_icons"]}'
            text_area_xpath = f'{review_xpath}{XPathes["text_area"]}'
            answer_xpath = f'{review_xpath}{XPathes["answer"]}'
            # Getting stars
            stars = len(self.driver.find_elements(By.XPATH, star_list_xpath))

            # Answer only for 5-star reviews
            if stars == 5:
                vendor_code = self.driver.find_element(By.XPATH, vendor_code_xpath).text
                # Open answer window
                self.driver.find_elements(By.XPATH, circle_icons_xpath)[0].click()
                text_area = self.driver.find_element(By.XPATH, text_area_xpath)
                answer = create_template("Шаблон.xlsx", vendor_code)

                # When we have no answer -> go to next review
                if answer[:6] == "Ошибка":
                    print(answer)
                    continue
                # Fill text area with answer and answer to the user
                text_area.send_keys(answer)
                self.click_on_item_xpath(answer_xpath)
                print(f"{i + 1:0>3} answered: {answer}")

        # Last page has no arrow to next page
        if len(self.driver.find_elements(By.XPATH, XPathes["arrow_to_next_page"])) == 0:
            return
        self.click_on_item_xpath(XPathes["arrow_to_next_page"])

        # Wait for page update
        time.sleep(3)
        self.answer_on_reviews()
