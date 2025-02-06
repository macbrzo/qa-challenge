from __future__ import annotations

import re
import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


class BaseElement:
    def __init__(
        self,
        driver: WebDriver,
        locator: str | None = None,
        parent: BaseElement | None = None,
        web_element: WebElement | None = None,
        timeout: int = config.global_timeout,
        logger=None,
    ):
        if not (web_element or locator):
            raise ValueError("Either locator or web_element must be provided")

        self.driver = driver
        self.locator = None if not locator else self.best_locator(locator=locator)
        self.web_element = web_element
        self.parent = parent
        self.timeout = timeout
        self.logger = logger

    def _get_location_context(self) -> WebDriver | WebElement:
        if self.parent:
            return self.parent.element
        return self.driver

    @staticmethod
    def best_locator(*, locator: str) -> tuple[str, str]:
        pattern = r"(?P<by>css|xpath)=(?P<selector>.+)"
        matches = re.match(pattern, locator)
        if not matches:
            raise AttributeError(f"Wrong locator provided {locator=}")
        by = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
        }[matches.group("by")]
        return by, matches.group("selector")

    @property
    def element(self) -> WebElement:
        if self.web_element:
            return self.web_element

        location_context = self._get_location_context()
        try:
            return WebDriverWait(
                driver=location_context,
                timeout=self.timeout,
                poll_frequency=0.2,
            ).until(EC.presence_of_element_located(self.locator))
        except TimeoutException:
            raise TimeoutException(f"Element not found: {self.locator}")

    def is_present(self) -> bool:
        if self.web_element:
            return self.web_element.is_displayed()

        location_context = self._get_location_context()
        element = location_context.find_elements(*self.locator)
        return bool(element)

    def click(self, attempts: int = 5) -> None:
        element = self.element
        if not element.is_enabled():
            raise TimeoutException(f"Element not enabled: {self.locator}")

        exception = None
        for _ in range(attempts):
            try:
                element.click()
                break
            except ElementClickInterceptedException as e:
                if not exception:
                    exception = e
                time.sleep(1)
        else:
            raise exception from None

    def find_all_elements_in_viewport(self) -> list[BaseElement]:
        elements = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_all_elements_located(self.locator)
        )

        js_script = """
        function isInViewport(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        }
        return isInViewport(arguments[0]);
        """
        visible_elements = []
        for element in elements:
            if self.driver.execute_script(js_script, element):
                visible_elements.append(BaseElement(driver=self.driver, web_element=element))
        return visible_elements

    def send_keys(self, value: str) -> None:
        element = self.element
        element.clear()
        element.send_keys(value)

    def wait_for_element_to_be_visible(self, timeout: int = 10) -> None:
        location_context = self._get_location_context()
        WebDriverWait(location_context, timeout=timeout).until(EC.visibility_of(self.element))
