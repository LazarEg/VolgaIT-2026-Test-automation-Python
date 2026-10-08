import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class FormFieldsPage(BasePage):
    URL = "https://practice-automation.com/form-fields/"

    NAME_INPUT = (By.ID, "name-input")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#feedbackForm input[type='password']")
    EMAIL_INPUT = (By.ID, "email")
    MESSAGE_INPUT = (By.ID, "message")
    SUBMIT_BUTTON = (By.ID, "submit-btn")

    AUTOMATION_TOOLS_LIST = (By.CSS_SELECTOR, "#feedbackForm ul > li")

    @allure.step("Открыть страницу Form Fields")
    def open_page(self):
        self.open(self.URL)

    @allure.step("Заполнить поле Name: {value}")
    def fill_name(self, value: str):
        self.type(self.NAME_INPUT, value)

    @allure.step("Заполнить поле Password")
    def fill_password(self, value: str):
        self.type(self.PASSWORD_INPUT, value)

    @allure.step("Заполнить поле Email: {value}")
    def fill_email(self, value: str):
        self.type(self.EMAIL_INPUT, value)

    @allure.step("Заполнить поле Message")
    def fill_message(self, value: str):
        self.type(self.MESSAGE_INPUT, value)

    @allure.step("Нажать Submit")
    def submit(self):
        self.click(self.SUBMIT_BUTTON)

    @allure.step("Получить список инструментов Automation tools")
    def get_automation_tools(self) -> list[str]:
        elements = self.find_all(self.AUTOMATION_TOOLS_LIST)
        tools = [el.text.strip() for el in elements if el.text.strip()]
        allure.attach(
            "\n".join(tools),
            name="Automation tools",
            attachment_type=allure.attachment_type.TEXT,
        )
        return tools

    @allure.step("Получить Automation tools одной строкой через запятую")
    def get_automation_tools_as_string(self, separator: str = ", ") -> str:
        return separator.join(self.get_automation_tools())

    def get_message_value(self) -> str:
        return self.find(self.MESSAGE_INPUT).get_attribute("value")

    def get_name_value(self) -> str:
        return self.find(self.NAME_INPUT).get_attribute("value")

    def get_email_value(self) -> str:
        return self.find(self.EMAIL_INPUT).get_attribute("value")

    def is_message_field_visible(self) -> bool:
        return self.is_visible(self.MESSAGE_INPUT)

    def is_automation_tools_visible(self) -> bool:
        return self.is_visible(self.AUTOMATION_TOOLS_LIST)

    def is_submit_button_visible(self) -> bool:
        return self.is_visible(self.SUBMIT_BUTTON)

    def is_form_valid(self) -> bool:
        return self.driver.execute_script(
            "return document.getElementById('feedbackForm').checkValidity();"
        )

    def is_alert_present(self, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            return True
        except Exception:
            return False

    def get_alert_text(self) -> str:
        try:
            return self.driver.switch_to.alert.text
        except Exception:
            return ""

    def accept_alert(self):
        try:
            self.driver.switch_to.alert.accept()
        except Exception:
            pass
