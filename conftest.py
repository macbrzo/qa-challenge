import os
from datetime import datetime
from typing import Generator

import pytest
from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from webdriver_manager.chrome import ChromeDriverManager

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

# devices = [
#     "iPhone X",
# ]
#


@pytest.fixture(params=devices)
def driver(request) -> Generator[Chrome, None, None]:
    mobile_emulation = {"deviceName": request.param}
    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    service = ChromeService(ChromeDriverManager().install())
    driver = Chrome(options=chrome_options, service=service)
    yield driver
    test_name = request.node.nodeid.replace("::", "_").replace("/", "_")
    take_screenshot(driver, test_name)
    driver.close()


#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_protocol(item):
#     """Make test name available globally for screenshot purposes."""
#     pytest.current_test = item.nodeid
#     yield
#


def take_screenshot(driver, test_name: str, screenshot_dir: str = "screenshots"):
    """Helper function to capture and save a screenshot."""
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(filepath)
    print(f"Screenshot saved at {filepath}")
