import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер: chrome или firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск в headless-режиме",
    )


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")

    if browser == "firefox":
        options = FirefoxOptions()
        options.page_load_strategy = "eager"
        if headless:
            options.add_argument("--headless")
        drv = webdriver.Firefox(options=options)
    else:
        options = ChromeOptions()
        options.page_load_strategy = "eager"
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if headless:
            options.add_argument("--headless=new")
        drv = webdriver.Chrome(options=options)

    drv.implicitly_wait(0)
    yield drv
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                try:
                    driver.switch_to.alert.dismiss()
                except Exception:
                    pass

                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                filename = f"{item.name}.png"
                path = os.path.join(screenshot_dir, filename)
                driver.save_screenshot(path)
                allure.attach.file(
                    path,
                    name=f"Скриншот_{item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
