from typing import Generator

import pytest
from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

import config
from libs.core.browser_ops import take_screenshot

devices = [
    "iPhone X",
    "iPhone 14 Pro Max",
    "Pixel 7",
    "Pixel 2",
    "Galaxy S5",
    "iPad",
    "iPad Pro",
    "Samsung Galaxy S20 Ultra",
]


@pytest.fixture(scope="session")
def chrome_service() -> Generator[ChromeService, None, None]:
    if config.remote_url:
        raise NotImplementedError("Remote not implemented")
    else:
        service = ChromeService(ChromeDriverManager().install())
    yield service


@pytest.fixture(params=devices)
def chrome_mobile_driver(request, chrome_service) -> Generator[WebDriver, None, None]:
    device = request.param

    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": device})

    driver = Chrome(service=chrome_service, options=chrome_options)
    driver.implicitly_wait(time_to_wait=2)
    yield driver

    test_name = request.node.nodeid.replace("::", "_").replace("/", "_")
    take_screenshot(driver=driver, test_name=test_name)
    driver.quit()
