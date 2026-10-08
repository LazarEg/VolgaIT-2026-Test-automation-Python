from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        return self.find(locator).text

    def is_visible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: self._fully_visible(d, locator)
            )
            return True
        except Exception:
            return False

    def is_invisible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: not self._fully_visible(d, locator)
            )
            return True
        except Exception:
            return False

    @staticmethod
    def _fully_visible(driver, locator) -> bool:
        try:
            elements = driver.find_elements(*locator)
            if not elements:
                return False
            return driver.execute_script(
                """
                var el = arguments[0];
                if (!el) return false;
                var cur = el;
                while (cur) {
                    var s = window.getComputedStyle(cur);
                    if (s.display === 'none') return false;
                    if (s.visibility === 'hidden') return false;
                    if (parseFloat(s.opacity) === 0) return false;
                    cur = cur.parentElement;
                }
                return true;
                """,
                elements[0],
            )
        except Exception:
            return False
