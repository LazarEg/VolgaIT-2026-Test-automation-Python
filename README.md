# UI-автотесты для practice-automation.com

Проект автоматизации UI-тестов на Python + Selenium + Pytest для сайта [practice-automation.com](https://practice-automation.com/).

## Стек

- Python 3.12+ (проект разработан и протестирован на 3.13)
- Selenium 4
- Pytest
- Allure (отчётность)
- Page Object Model

## Структура проекта

```
.
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── calendars_page.py
│   ├── modals_page.py
│   ├── ads_page.py
│   └── form_fields_page.py
├── tests/
│   ├── __init__.py
│   ├── test_calendars.py
│   ├── test_modals.py
│   ├── test_ads.py
│   └── test_form_fields.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

## Установка

### 1. Создать виртуальное окружение

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Установить Allure CLI

Allure нужен только для просмотра отчёта. Есть несколько способов установки.

**Вариант 1 — Scoop (Windows):**

```bash
scoop install allure
```

**Вариант 2 — вручную (Windows, macOS, Linux):**

1. Скачать ZIP с https://github.com/allure-framework/allure2/releases
2. Распаковать в удобное место (например, `C:\tools\allure`)
3. Добавить папку `bin` в переменную `PATH`
4. Проверить установку: `allure --version`

**Вариант 3 — Homebrew (macOS):**

```bash
brew install allure
```

## Запуск тестов

Все тесты:

```bash
pytest tests/ -v
```

Отдельные файлы:

```bash
pytest tests/test_calendars.py -v
pytest tests/test_modals.py -v
pytest tests/test_ads.py -v
pytest tests/test_form_fields.py -v
```

Дополнительные параметры:

```bash
pytest tests/ -v --headless
pytest tests/ -v --browser firefox
```

### Чистый прогон перед сдачей отчёта

Перед новым прогоном удалите артефакты предыдущего — иначе в Allure-отчёт
попадут результаты старых запусков, и статистика будет некорректной.

**Windows (cmd):**

```bash
rmdir /s /q allure-results
rmdir /s /q screenshots
```

**Windows (PowerShell):**

```powershell
Remove-Item -Recurse -Force allure-results, screenshots -ErrorAction SilentlyContinue
```

**macOS / Linux:**

```bash
rm -rf allure-results screenshots
```

После этого:

```bash
pytest tests/ -v
allure serve allure-results
```

## Allure-отчёт

```bash
allure serve allure-results
```

Отчёт содержит названия тестов, шаги, severity и скриншоты, автоматически снятые при падениях.

Если нужен статичный HTML-отчёт (без запуска локального сервера):

```bash
allure generate allure-results -o allure-report --clean
```

Открыть `allure-report/index.html` в браузере.

## Тест-кейсы

### Календари — 12 тестов

Позитивные:

1. Страница открывается, title корректен
2. Поле ввода даты отображается
3. Кнопка Submit отображается
4. Дата вводится и сохраняется в поле
5. Поле принимает разные валидные даты (параметризованный, 4 набора)
6. Submit с валидной датой показывает сообщение об успехе
7. Сообщение об успехе содержит «Thank you»
8. После успешного submit отображается отправленная дата

Негативные:

1. Submit с пустой формой не показывает сообщение об успехе
2. Submit с текстом вместо даты не показывает успех
3. Submit с датой в формате DD.MM.YYYY не показывает успех
4. Submit с несуществующей датой (месяц 13) не показывает успех

### Модальные окна — 14 тестов

Позитивные:

1. Страница открывается, title корректен
2. Кнопка «Simple Modal» отображается
3. Кнопка «Form Modal» отображается
4. Simple Modal открывается по клику
5. Simple Modal содержит правильный заголовок
6. Simple Modal содержит правильный текст
7. Form Modal открывается по клику
8. Form Modal содержит правильный заголовок
9. Поля формы (Name, Email, Message) отображаются
10. Успешная отправка формы показывает сообщение об успехе

Негативные:

1. Simple Modal не отображается до клика
2. Form Modal не отображается до клика
3. После закрытия Simple Modal не отображается
4. Submit пустой Form Modal не показывает сообщение об успехе

### Реклама — 13 тестов

Позитивные:

1. Страница открывается, title корректен
2. Текст-счётчик «An ad will appear in» отображается
3. Предупреждение про adblock отображается
4. Рекламный попап появляется автоматически
5. Заголовок рекламы — «Hi»
6. Тело рекламы содержит «I am an ad.»
7. Кнопка закрытия отображается
8. Клик по кнопке закрытия скрывает рекламу
9. После закрытия реклама не появляется повторно

Негативные:

1. Реклама не отображается сразу после загрузки
2. Реклама не появляется до завершения счётчика
3. Кнопка закрытия не видна до появления рекламы
4. Закрытая реклама не возвращается в течение 5 секунд

### Форма — 15 тестов

Позитивные:

1. Страница открывается, title корректен
2. Поле Message отображается
3. Список Automation tools отображается
4. Кнопка Submit отображается
5. Список Automation tools содержит ожидаемые инструменты
6. Поле Message принимает текст
7. Поля Name и Email принимают значения
8. Поле Message заполняется списком Automation tools через запятую
9. Submit с валидными данными показывает alert «Message received!»

Негативные:

1. Форма невалидна без обязательного поля Name
2. Форма валидна, когда Name заполнено
3. Submit без Name не показывает alert
4. Поле Message пустое при открытии страницы
5. Поле Message очищается

## Спецзадание

> На странице с формой поле Message заполнить следующим образом: получить средствами Selenium список элементов из раздела Automation Tools, преобразовать в текст и заполнить поле полученным списком через запятую.

Реализовано в тесте `test_fill_message_with_automation_tools`:

1. Собираются все `<li>` внутри `#feedbackForm ul`.
2. Названия склеиваются через `", "`.
3. Строка вводится в поле `#message`.
4. Проверяется, что поле содержит именно эту строку.

Ожидаемый результат: `Selenium, Playwright, Cypress, Appium, Katalon Studio`.

## Скриншоты при падении

Работают автоматически благодаря хуку `pytest_runtest_makereport` в `conftest.py`. При падении любого теста делается скриншот, сохраняется в `screenshots/` и прикрепляется к Allure-отчёту.
