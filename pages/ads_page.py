from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AdsPage(BasePage):
    URL = "https://practice-automation.com/ads/"

    AD_CONTAINER = (By.ID, "popmake-1272")
    AD_TITLE = (By.ID, "pum_popup_title_1272")
    AD_BODY = (By.CSS_SELECTOR, "#popmake-1272 .pum-content")
    AD_CLOSE = (By.CSS_SELECTOR, "#popmake-1272 .pum-close")

    COUNTDOWN_TEXT = (By.XPATH, "//p[contains(text(), 'An ad will appear')]")
    WARNING_TEXT = (By.XPATH, "//strong[contains(text(), 'ad blockers')]")

    def open_page(self):
        self.open(self.URL)

    def wait_for_ad(self, timeout: int = 15) -> bool:
        return self.is_visible(self.AD_CONTAINER, timeout=timeout)

    def close_ad(self):
        self.click(self.AD_CLOSE)

    def is_ad_visible(self, timeout: int = 3) -> bool:
        return self.is_visible(self.AD_CONTAINER, timeout=timeout)

    def is_ad_invisible(self, timeout: int = 3) -> bool:
        return self.is_invisible(self.AD_CONTAINER, timeout=timeout)

    def is_ad_close_button_visible(self, timeout: int = 3) -> bool:
        return self.is_visible(self.AD_CLOSE, timeout=timeout)

    def is_countdown_text_visible(self) -> bool:
        return self.is_visible(self.COUNTDOWN_TEXT)

    def is_warning_text_visible(self) -> bool:
        return self.is_visible(self.WARNING_TEXT)

    def get_ad_title(self) -> str:
        return self.get_text(self.AD_TITLE)

    def get_ad_body(self) -> str:
        return self.get_text(self.AD_BODY)

    def get_countdown_text(self) -> str:
        return self.get_text(self.COUNTDOWN_TEXT)
