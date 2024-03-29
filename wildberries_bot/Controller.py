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
    "reviews": r'(//div[contains(@class, "Card__wrapper__")])',
    "review_counter": r'(//span[contains(@class, "Tab--page__count")]//span[@data-name="Counter"])[1]',
    "arrow_to_next_page": r'//button[contains(@class, "Pagination-icon-button")]//*[name()="path" and contains(@d, "M7.58586")]/../..',
    "star_list": r'//li[contains(@class, "Rating-stars-list")]',
    "active_star": r'//span[@style="width: 16px;"]',
    "vendor_code": r'//span[text()="Артикул продавца"]/../../span[contains(@class, "Text")]',
    "answer_and_go_to_inner": r'//a[contains(@class, "Button-link--link-darkPurple")]',
    "text_area": r'//textarea',
    "answer": r'//span[text()="Ответить" and contains(@class, "Button-link__text")]',
    "notification": r'//div[contains(@class, "Notifications-modals-container")]'
}


class Controller:
    def __init__(self):
        s = Service('./chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={UserAgent(use_external_data=True).chrome}")
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=s, options=options)

    def __check_creation(self, xpath: str) -> None:
        while len(self.driver.find_elements(By.XPATH, xpath)) == 0:
            time.sleep(5)

    def click_on_item_xpath(self, xpath: str) -> None:
        """
        This method clicks on element by Xpath after checking creation
        """
        self.__check_creation(xpath)
        try:
            item = self.driver.find_element(By.XPATH, xpath)
            item.click()
        except Exception as e:
            timer = 5
            print(f'[ERROR] Can\'t click the element. Trying again in {timer} seconds.')
            time.sleep(timer)

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
        # Exit trigger
        reviews_count = self.get_reviews_counter()
        if reviews_count == 0:
            print("[ERROR] No reviews on page!")
            return
        print(f"[INFO] Reviews count: {reviews_count}")
        self.driver.execute_script("window.scrollTo(0, 0);")
        print("[INFO] Scrolling to the top of page")
        reviews = self.get_reviews()
        for i, review in enumerate(reviews):
            # Set review to the bottom of screen
            self.driver.execute_script("arguments[0].scrollIntoView(false);", review)
            # Unique XPathes for reviews
            review_xpath = f'{XPathes["reviews"]}[{i + 1}]'
            star_list_xpath = f'{review_xpath}{XPathes["star_list"]}{XPathes["active_star"]}'
            vendor_code_xpath = f'{review_xpath}{XPathes["vendor_code"]}'
            answer_to_inner_xpath = f'{review_xpath}{XPathes["answer_and_go_to_inner"]}'
            text_area_xpath = f'{review_xpath}{XPathes["text_area"]}'
            answer_xpath = f'{review_xpath}{XPathes["answer"]}'
            # Getting stars
            stars = len(self.driver.find_elements(By.XPATH, star_list_xpath))
            print(f"------------------ Review {i + 1:0>3}----------------------\n"
                  f"[INFO] Stars counter for current review: {stars}")
            # Answer only for 5-star reviews
            if stars != 5:
                print(f"[INFO] Not enough stars [{stars} != 5]. Continue...")
                continue
            vendor_code = self.driver.find_element(By.XPATH, vendor_code_xpath).text
            print(f"[INFO] Vendor code for this review: {vendor_code}")
            # Open answer window
            self.click_on_item_xpath(answer_to_inner_xpath)
            print(text_area_xpath)
            text_area = self.driver.find_element(By.XPATH, text_area_xpath)
            print(f"[INFO] Text area for this review: {text_area}")
            answer = create_template("Шаблон.xlsx", vendor_code)

            # When we have no answer -> go to next review
            if answer[:6] == "Ошибка":
                print(answer)
                continue
            # Fill text area with answer and answer to the user
            text_area.send_keys(answer)
            self.click_on_item_xpath(answer_xpath)
            print(f"[INFO] {i + 1:0>3} answered: {answer}")
        # Last page has no arrow to next page
        if len(self.driver.find_elements(By.XPATH, XPathes["arrow_to_next_page"])) == 0:
            print("[INFO] Can't find arrow to next page. This is the end of execution.")
            return
        self.click_on_item_xpath(XPathes["arrow_to_next_page"])

        # Wait for page update
        time.sleep(3)
        self.answer_on_reviews()
