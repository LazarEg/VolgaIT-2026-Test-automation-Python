import allure

from pages.modals_page import ModalsPage


@allure.feature("Модальные окна")
class TestModals:

    @allure.story("Открытие страницы")
    @allure.title("Страница модальных окон открывается, title корректен")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_page(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        assert "Modals" in driver.title

    @allure.story("UI-элементы")
    @allure.title("Кнопка 'Simple Modal' отображается")
    def test_simple_modal_button_displayed(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        assert page.is_simple_modal_button_displayed()

    @allure.story("UI-элементы")
    @allure.title("Кнопка 'Form Modal' отображается")
    def test_form_modal_button_displayed(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        assert page.is_form_modal_button_displayed()

    @allure.story("Simple Modal")
    @allure.title("Simple Modal открывается по клику")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_simple_modal_opens(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        page.open_simple_modal()
        assert page.is_simple_modal_visible(), "Simple Modal не открылась"

    @allure.story("Simple Modal")
    @allure.title("Simple Modal содержит правильный заголовок")
    def test_simple_modal_title(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        page.open_simple_modal()
        assert page.is_simple_modal_visible()
        assert page.get_simple_modal_title() == "Simple Modal"

    @allure.story("Simple Modal")
    @allure.title("Simple Modal содержит правильный текст")
    def test_simple_modal_body_text(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        page.open_simple_modal()
        assert page.is_simple_modal_visible()
        assert "simple modal" in page.get_simple_modal_body().lower()

    @allure.story("Form Modal")
    @allure.title("Form Modal открывается по клику")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_form_modal_opens(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        page.open_form_modal()
        assert page.is_form_modal_visible(), "Form Modal не открылась"

    @allure.story("Form Modal")
    @allure.title("Form Modal содержит правильный заголовок")
    def test_form_modal_title(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        page.open_form_modal()
        assert page.is_form_modal_visible()
        assert page.get_form_modal_title() == "Modal Containing A Form"

    @allure.story("Form Modal")
    @allure.title("Поля формы (Name, Email, Message) отображаются")
    def test_form_modal_fields_displayed(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        page.open_form_modal()
        assert page.is_form_modal_visible()
        assert page.is_visible(page.NAME_INPUT)
        assert page.is_visible(page.EMAIL_INPUT)
        assert page.is_visible(page.MESSAGE_INPUT)

    @allure.story("Form Modal")
    @allure.title("Успешная отправка формы показывает сообщение об успехе")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_form_modal_submit_success(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        page.open_form_modal()
        page.is_form_modal_visible()
        page.fill_form(
            name="Ivan Ivanov",
            email="ivan@example.com",
            message="Test message",
        )
        page.submit_form()
        assert page.is_form_success_visible(
            timeout=10
        ), "Сообщение об успехе не появилось"

    @allure.story("Негативные проверки")
    @allure.title("Simple Modal не отображается до клика")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_simple_modal_hidden_initially(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        assert page.is_simple_modal_invisible(timeout=2), "Simple Modal видна до клика"

    @allure.story("Негативные проверки")
    @allure.title("Form Modal не отображается до клика")
    def test_form_modal_hidden_initially(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        assert page.is_form_modal_invisible(timeout=2), "Form Modal видна до клика"

    @allure.story("Негативные проверки")
    @allure.title("После закрытия Simple Modal не отображается")
    def test_simple_modal_hidden_after_close(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        page.open_simple_modal()
        assert page.is_simple_modal_visible()
        page.close_simple_modal()
        assert page.is_simple_modal_invisible(
            timeout=3
        ), "Simple Modal всё ещё видна после закрытия"

    @allure.story("Негативные проверки")
    @allure.title("Submit пустой Form Modal не показывает сообщение об успехе")
    def test_form_modal_empty_submit_no_success(self, driver):
        page = ModalsPage(driver)
        page.open_page()
        page.open_form_modal()
        page.is_form_modal_visible()
        page.submit_form()
        assert not page.is_form_success_visible(
            timeout=3
        ), "Форма отправилась с пустым обязательным полем Name"
