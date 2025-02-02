from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver):
        """
        BasePage class for common page interactions.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        self.driver = driver

    def __repr__(self):
        return self.get_title()

    def wait_for_page_to_load(self, *, timeout=10):
        try:
            WebDriverWait(
                self.driver,
                timeout,
                poll_frequency=0.5,
                ignored_exceptions=[StaleElementReferenceException],
            ).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            raise TimeoutException(
                f"Page did not load completely within the given {timeout=}."
            )

    def scroll_by_screen(self, *, screens_count: float):
        # it scrolls from current position
        screen_height = self.driver.execute_script("return window.innerHeight")
        self.driver.execute_script(
            f"window.scrollBy(0, {screens_count * screen_height});"
        )
        self.wait_for_page_to_load()

    def open_url(self, *, url: str):
        """Opens the given URL in the browser."""
        self.driver.get(url)
        self.wait_for_page_to_load()

    def get_title(self) -> str:
        """Returns the current page title."""
        return self.driver.title

    def take_screenshot(self, screenshot_name: str):
        self.driver.save_screenshot(screenshot_name)
