import allure

from pages.ads_page import AdsPage


@allure.feature("Рекламные окна")
class TestAds:

    @allure.story("Открытие страницы")
    @allure.title("Страница Ads открывается, title корректен")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_page(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert "Ads" in driver.title

    @allure.story("UI-элементы")
    @allure.title("Текст-счётчик 'An ad will appear in' отображается")
    def test_countdown_text_present(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert page.is_countdown_text_visible()
        assert "An ad will appear in" in page.get_countdown_text()

    @allure.story("UI-элементы")
    @allure.title("Предупреждение про adblock отображается")
    def test_warning_text_present(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert page.is_warning_text_visible()

    @allure.story("Появление рекламы")
    @allure.title("Рекламный попап появляется автоматически")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ad_appears_automatically(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert page.wait_for_ad(timeout=15), "Рекламный попап не появился за 15 сек"

    @allure.story("Содержимое рекламы")
    @allure.title("Заголовок рекламного попапа — 'Hi'")
    def test_ad_title(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert page.wait_for_ad(timeout=15)
        assert page.get_ad_title() == "Hi"

    @allure.story("Содержимое рекламы")
    @allure.title("Тело рекламного попапа содержит 'I am an ad.'")
    def test_ad_body_text(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert page.wait_for_ad(timeout=15)
        assert "I am an ad." in page.get_ad_body()

    @allure.story("Управление рекламой")
    @allure.title("Кнопка закрытия рекламы отображается")
    def test_ad_close_button_visible(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert page.wait_for_ad(timeout=15)
        assert page.is_ad_close_button_visible()

    @allure.story("Управление рекламой")
    @allure.title("Клик по кнопке закрытия скрывает рекламу")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ad_closes_on_close_button(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert page.wait_for_ad(timeout=15)
        page.close_ad()
        assert page.is_ad_invisible(timeout=3), "Реклама не закрылась"

    @allure.story("Управление рекламой")
    @allure.title("После закрытия реклама не появляется повторно")
    def test_ad_stays_closed(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert page.wait_for_ad(timeout=15)
        page.close_ad()
        assert page.is_ad_invisible(timeout=3)
        assert page.is_ad_invisible(timeout=3), "Реклама вернулась после закрытия"

    @allure.story("Негативные проверки")
    @allure.title("Реклама не отображается сразу после загрузки страницы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ad_hidden_initially(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert page.is_ad_invisible(timeout=2), "Реклама появилась сразу после загрузки"

    @allure.story("Негативные проверки")
    @allure.title("Реклама не появляется до завершения счётчика (3 сек)")
    def test_ad_hidden_before_countdown_finishes(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert page.is_ad_invisible(
            timeout=3
        ), "Реклама появилась раньше, чем должен завершиться счётчик"

    @allure.story("Негативные проверки")
    @allure.title("Кнопка закрытия рекламы не видна до её появления")
    def test_ad_close_button_hidden_initially(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert not page.is_ad_close_button_visible(
            timeout=2
        ), "Кнопка закрытия видна до появления рекламы"

    @allure.story("Негативные проверки")
    @allure.title("Закрытая реклама не возвращается в течение 5 секунд")
    def test_ad_does_not_reappear_after_close(self, driver):
        page = AdsPage(driver)
        page.open_page()
        assert page.wait_for_ad(timeout=15)
        page.close_ad()
        assert page.is_ad_invisible(timeout=3)
        assert page.is_ad_invisible(timeout=5), "Реклама вернулась после закрытия"
