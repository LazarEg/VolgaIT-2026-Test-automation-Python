import allure
import pytest

from pages.calendars_page import CalendarsPage


@allure.feature("Календари")
class TestCalendars:

    @allure.story("Открытие страницы")
    @allure.title("Страница календарей открывается, title корректен")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_page(self, driver):
        page = CalendarsPage(driver)
        page.open_page()
        assert "Calendars" in driver.title

    @allure.story("UI-элементы")
    @allure.title("Поле ввода даты отображается")
    def test_date_field_displayed(self, driver):
        page = CalendarsPage(driver)
        page.open_page()
        assert page.is_date_field_displayed()

    @allure.story("UI-элементы")
    @allure.title("Кнопка Submit отображается")
    def test_submit_button_displayed(self, driver):
        page = CalendarsPage(driver)
        page.open_page()
        assert page.is_submit_button_displayed()

    @allure.story("Ввод даты")
    @allure.title("Дата вводится и сохраняется в поле")
    def test_enter_date_saves_value(self, driver):
        page = CalendarsPage(driver)
        page.open_page()
        page.enter_date("2024-01-15")
        assert page.get_date_value() == "2024-01-15"

    @allure.story("Ввод даты")
    @allure.title("Поле принимает разные валидные даты")
    @pytest.mark.parametrize(
        "date_value",
        ["2024-01-01", "2024-06-15", "2024-12-31", "2000-02-29"],
    )
    def test_enter_various_dates(self, driver, date_value):
        page = CalendarsPage(driver)
        page.open_page()
        page.enter_date(date_value)
        assert page.get_date_value() == date_value

    @allure.story("Отправка формы")
    @allure.title("Submit с валидной датой показывает сообщение об успехе")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_valid_date_shows_success(self, driver):
        page = CalendarsPage(driver)
        page.open_page()
        page.enter_date("2024-01-15")
        page.submit()
        assert page.is_success_displayed(), "Сообщение об успехе не появилось"

    @allure.story("Отправка формы")
    @allure.title("Сообщение об успехе содержит 'Thank you'")
    def test_success_message_text(self, driver):
        page = CalendarsPage(driver)
        page.open_page()
        page.enter_date("2024-01-15")
        page.submit()
        assert page.is_success_displayed()
        assert "Thank you" in page.get_success_text()

    @allure.story("Отправка формы")
    @allure.title("После успешного submit отображается отправленная дата")
    def test_submitted_date_shown_in_result(self, driver):
        page = CalendarsPage(driver)
        page.open_page()
        page.enter_date("2024-01-15")
        page.submit()
        assert page.is_success_displayed()
        assert "2024-01-15" in page.get_submission_text()

    @allure.story("Негативные проверки")
    @allure.title("Submit с пустой формой не показывает сообщение об успехе")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_empty_form_no_success(self, driver):
        page = CalendarsPage(driver)
        page.open_page()
        page.submit()
        assert not page.is_success_displayed(
            timeout=3
        ), "Сообщение об успехе появилось при пустой форме"

    @allure.story("Негативные проверки")
    @allure.title("Submit с текстом вместо даты не показывает сообщение об успехе")
    def test_submit_text_instead_of_date(self, driver):
        page = CalendarsPage(driver)
        page.open_page()
        page.enter_date("not-a-date")
        page.submit()
        assert not page.is_success_displayed(
            timeout=3
        ), "Сообщение об успехе появилось при неверном вводе"

    @allure.story("Негативные проверки")
    @allure.title(
        "Submit с датой в формате DD.MM.YYYY не показывает сообщение об успехе"
    )
    def test_submit_wrong_date_format(self, driver):
        page = CalendarsPage(driver)
        page.open_page()
        page.enter_date("15.01.2024")
        page.submit()
        assert not page.is_success_displayed(
            timeout=3
        ), "Сообщение об успехе появилось при дате в формате DD.MM.YYYY"

    @allure.story("Негативные проверки")
    @allure.title(
        "Submit с несуществующей датой (месяц 13) не показывает сообщение об успехе"
    )
    def test_submit_invalid_date(self, driver):
        page = CalendarsPage(driver)
        page.open_page()
        page.enter_date("2024-13-45")
        page.submit()
        assert not page.is_success_displayed(
            timeout=3
        ), "Сообщение об успехе появилось при несуществующей дате"
