import allure

from pages.form_fields_page import FormFieldsPage


@allure.feature("Форма Form Fields")
class TestFormFields:

    @allure.story("Открытие страницы")
    @allure.title("Страница Form Fields открывается, title корректен")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_page(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        assert "Form Fields" in driver.title

    @allure.story("UI-элементы")
    @allure.title("Поле Message отображается")
    def test_message_field_visible(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        assert page.is_message_field_visible()

    @allure.story("UI-элементы")
    @allure.title("Список Automation tools отображается")
    def test_automation_tools_visible(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        assert page.is_automation_tools_visible()

    @allure.story("UI-элементы")
    @allure.title("Кнопка Submit отображается")
    def test_submit_button_visible(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        assert page.is_submit_button_visible()

    @allure.story("Automation tools")
    @allure.title("Список Automation tools содержит ожидаемые инструменты")
    def test_automation_tools_content(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        tools = page.get_automation_tools()
        expected = ["Selenium", "Playwright", "Cypress", "Appium", "Katalon Studio"]
        assert tools == expected, f"Ожидалось {expected}, получено {tools}"

    @allure.story("Заполнение формы")
    @allure.title("Поле Message принимает текст")
    def test_fill_message(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        page.fill_message("Hello, world!")
        assert page.get_message_value() == "Hello, world!"

    @allure.story("Заполнение формы")
    @allure.title("Поля Name и Email принимают значения")
    def test_fill_name_and_email(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        page.fill_name("Ivan Ivanov")
        page.fill_email("ivan@example.com")
        assert page.get_name_value() == "Ivan Ivanov"
        assert page.get_email_value() == "ivan@example.com"

    @allure.story("Спецзадание: Automation Tools → Message")
    @allure.title("Поле Message заполняется списком Automation tools через запятую")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_fill_message_with_automation_tools(self, driver):
        page = FormFieldsPage(driver)

        with allure.step("Открыть страницу Form Fields"):
            page.open_page()

        with allure.step("Получить список элементов Automation tools"):
            tools = page.get_automation_tools()
            assert len(tools) == 5, f"Ожидалось 5 инструментов, найдено {len(tools)}"

        with allure.step("Преобразовать список в текст через запятую"):
            expected = ", ".join(tools)
            assert expected == "Selenium, Playwright, Cypress, Appium, Katalon Studio"

        with allure.step(f"Заполнить поле Message строкой: {expected}"):
            page.fill_message(expected)

        with allure.step("Проверить, что поле Message содержит введённую строку"):
            assert page.get_message_value() == expected

    @allure.story("Отправка формы")
    @allure.title("Submit с валидными данными показывает alert 'Message received!'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_valid_form(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        page.fill_name("Ivan Ivanov")
        page.fill_email("ivan@example.com")
        page.fill_message(page.get_automation_tools_as_string())
        page.submit()

        assert page.is_alert_present(
            timeout=5
        ), "Alert 'Message received!' не появился после submit"

        with allure.step("Проверить текст alert"):
            alert_text = page.get_alert_text()
            assert (
                "Message received" in alert_text
            ), f"Неожиданный текст alert: {alert_text}"

        with allure.step("Закрыть alert"):
            page.accept_alert()

    @allure.story("Негативные проверки")
    @allure.title("Форма невалидна без обязательного поля Name")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_form_invalid_without_name(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        page.fill_email("ivan@example.com")
        page.fill_message("Test")
        assert not page.is_form_valid(), "Форма считается валидной без Name"

    @allure.story("Негативные проверки")
    @allure.title("Форма валидна, когда Name заполнено")
    def test_form_valid_with_name(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        page.fill_name("Ivan Ivanov")
        assert page.is_form_valid(), "Форма невалидна, хотя Name заполнено"

    @allure.story("Негативные проверки")
    @allure.title("Submit без Name не показывает alert")
    def test_submit_without_name_no_alert(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        page.fill_email("ivan@example.com")
        page.submit()
        assert not page.is_alert_present(
            timeout=2
        ), "Появился alert, хотя обязательное поле Name пустое"

    @allure.story("Негативные проверки")
    @allure.title("Поле Message пустое при открытии страницы")
    def test_message_empty_initially(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        assert page.get_message_value() == ""

    @allure.story("Негативные проверки")
    @allure.title("Поле Message очищается")
    def test_message_can_be_cleared(self, driver):
        page = FormFieldsPage(driver)
        page.open_page()
        page.fill_message("Some text")
        page.find(page.MESSAGE_INPUT).clear()
        assert page.get_message_value() == ""
