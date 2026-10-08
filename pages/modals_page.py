from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class ModalsPage(BasePage):
    URL = "https://practice-automation.com/modals/"

    SIMPLE_MODAL_BUTTON = (By.ID, "simpleModal")
    FORM_MODAL_BUTTON = (By.ID, "formModal")

    SIMPLE_MODAL = (By.ID, "popmake-1318")
    SIMPLE_MODAL_TITLE = (By.ID, "pum_popup_title_1318")
    SIMPLE_MODAL_BODY = (By.CSS_SELECTOR, "#popmake-1318 .pum-content")
    SIMPLE_MODAL_CLOSE = (By.CSS_SELECTOR, "#popmake-1318 .pum-close")

    FORM_MODAL = (By.ID, "popmake-674")
    FORM_MODAL_TITLE = (By.ID, "pum_popup_title_674")
    FORM_MODAL_CLOSE = (By.CSS_SELECTOR, "#popmake-674 .pum-close")

    NAME_INPUT = (By.ID, "g1051-name")
    EMAIL_INPUT = (By.ID, "g1051-email")
    MESSAGE_INPUT = (By.ID, "contact-form-comment-g1051-message")
    FORM_SUBMIT = (
        By.CSS_SELECTOR,
        "#popmake-674 button[type='submit'].pushbutton-wide",
    )

    FORM_EL = (By.CSS_SELECTOR, "#popmake-674 form.jetpack-contact-form__form")
    FORM_SUCCESS_CLASS = "submission-success"

    def open_page(self):
        self.open(self.URL)

    def open_simple_modal(self):
        self.click(self.SIMPLE_MODAL_BUTTON)

    def open_form_modal(self):
        self.click(self.FORM_MODAL_BUTTON)

    def close_simple_modal(self):
        self.click(self.SIMPLE_MODAL_CLOSE)

    def close_form_modal(self):
        self.click(self.FORM_MODAL_CLOSE)

    def fill_form(self, name=None, email=None, message=None):
        if name is not None:
            self.type(self.NAME_INPUT, name)
        if email is not None:
            self.type(self.EMAIL_INPUT, email)
        if message is not None:
            self.type(self.MESSAGE_INPUT, message)

    def submit_form(self):
        self.click(self.FORM_SUBMIT)

    def is_simple_modal_button_displayed(self) -> bool:
        return self.is_visible(self.SIMPLE_MODAL_BUTTON)

    def is_form_modal_button_displayed(self) -> bool:
        return self.is_visible(self.FORM_MODAL_BUTTON)

    def is_simple_modal_visible(self, timeout: int = 3) -> bool:
        return self.is_visible(self.SIMPLE_MODAL, timeout=timeout)

    def is_simple_modal_invisible(self, timeout: int = 3) -> bool:
        return self.is_invisible(self.SIMPLE_MODAL, timeout=timeout)

    def is_form_modal_visible(self, timeout: int = 3) -> bool:
        return self.is_visible(self.FORM_MODAL, timeout=timeout)

    def is_form_modal_invisible(self, timeout: int = 3) -> bool:
        return self.is_invisible(self.FORM_MODAL, timeout=timeout)

    def is_form_success_visible(self, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: self.FORM_SUCCESS_CLASS
                in (d.find_element(*self.FORM_EL).get_attribute("class") or "")
            )
            return True
        except Exception:
            return False

    def get_simple_modal_title(self) -> str:
        return self.get_text(self.SIMPLE_MODAL_TITLE)

    def get_simple_modal_body(self) -> str:
        return self.get_text(self.SIMPLE_MODAL_BODY)

    def get_form_modal_title(self) -> str:
        return self.get_text(self.FORM_MODAL_TITLE)
