from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.chrome.webdriver import WebDriver

from libs.core.ui import BaseElement

if TYPE_CHECKING:
    from ui.pages import BrowsePage


class MobileNavBar:
    def __init__(self, driver: WebDriver, parent_locator: str = "css=div.dShAUu", logger=None):
        self.driver = driver
        self.parent_locator = BaseElement(driver, locator=parent_locator)
        self.search_btn = BaseElement(
            driver, parent=self.parent_locator, locator="css=[href='/directory']"
        )
        self.logger = logger

    def navigate_to_search_page(self) -> BrowsePage:
        self.search_btn.click()
        from ui.pages import BrowsePage

        search_page = BrowsePage(driver=self.driver)
        search_page.wait_for_page_to_load()
        return search_page
