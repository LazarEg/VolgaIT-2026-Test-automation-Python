from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CalendarsPage(BasePage):
    URL = "https://practice-automation.com/calendars/"

    DATE_INPUT = (By.ID, "g1065-1-selectorenteradate")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit'].pushbutton-wide")
    SUCCESS_HEADER = (By.CSS_SELECTOR, "h4[id^='contact-form-success-header']")
    SUBMISSION_BLOCK = (By.CSS_SELECTOR, ".contact-form-submission")

    def open_page(self):
        self.open(self.URL)

    def enter_date(self, date_str: str):
        self.type(self.DATE_INPUT, date_str)

    def get_date_value(self) -> str:
        return self.find(self.DATE_INPUT).get_attribute("value")

    def is_date_field_displayed(self) -> bool:
        return self.is_visible(self.DATE_INPUT)

    def is_submit_button_displayed(self) -> bool:
        return self.is_visible(self.SUBMIT_BUTTON)

    def submit(self):
        self.click(self.SUBMIT_BUTTON)

    def is_success_displayed(self, timeout: int = 3) -> bool:
        return self.is_visible(self.SUCCESS_HEADER, timeout=timeout)

    def get_success_text(self) -> str:
        return self.get_text(self.SUCCESS_HEADER)

    def get_submission_text(self) -> str:
        return self.get_text(self.SUBMISSION_BLOCK)
