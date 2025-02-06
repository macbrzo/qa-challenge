from selenium.webdriver.chrome.webdriver import WebDriver

from ui.pages.twitch_base_page import TwitchTVPage


class HomePage(TwitchTVPage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
