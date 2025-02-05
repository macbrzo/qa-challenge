from typing import List

from selenium.webdriver import Keys

from libs.core.ui import BaseElement
from ui.pages.twitch_base_page import TwitchTVPage


class BrowsePage(TwitchTVPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.search_input = BaseElement(
            driver=driver,
            locator="xpath=//input[@placeholder='Search']",
        )
        self.search_btn = BaseElement(
            driver=driver,
            locator="css=[aria-label='Search Button']",
        )

        self.channels_btn = BaseElement(
            driver,
            locator="xpath=//div[text()='Channels']",
        )
        self.channels_container = BaseElement(
            driver,
            locator="xpath=//div[@role='list']/div[contains(@class, 'Layout')]/button",
        )

    def search_twitch(self, input_phrase: str) -> None:
        self.nav_bar.navigate_to_search_page()
        self.search_input.send_keys(value=input_phrase + Keys.RETURN)

    def navigate_to_channels(self) -> List[BaseElement]:
        self.channels_btn.click()
        return self.list_visible_channels()

    def list_visible_channels(self) -> List[BaseElement]:
        return self.channels_container.find_all_elements_in_viewport()
