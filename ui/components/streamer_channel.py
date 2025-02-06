import logging

from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from libs.core.ui import BaseElement


class StreamerChannel:
    def __init__(
        self,
        driver: WebDriver,
        parent_locator: str = "css=div#channel-live-overlay",
        logger=logging,
    ):
        self.driver = driver
        self.logger = logger
        self.parent_locator = BaseElement(driver, locator=parent_locator)
        # content gate
        # https://m.twitch.tv/vaelyth_
        # https://m.twitch.tv/protech
        self.content_gate = BaseElement(
            driver,
            locator="css=div[data-a-target='content-classification-gate-overlay']",
            parent=self.parent_locator,
        )
        self.start_watching_btn = BaseElement(
            driver,
            locator="css=button[data-a-target*='start-watching-button']",
            parent=self.content_gate,
        )
        self.video = BaseElement(driver, locator="css=video", parent=self.parent_locator)
        self.streamer_container = BaseElement(
            driver,
            locator="xpath=//div[contains(@class, 'streamInfoContainer')]",
            parent=self.parent_locator,
        )

    def is_video_started(self, *, timeout: int = 20) -> bool:
        try:
            WebDriverWait(self.driver, timeout=timeout).until(
                lambda d: d.execute_script(
                    "return arguments[0].readyState >= 4;", self.video.element
                )
            )
        except TimeoutException as e:
            self.logger.error(e)
            return False
        return True

    def handle_content_gate_popup(self) -> None:
        self.streamer_container.wait_for_element_to_be_visible()
        if self.content_gate.is_present():
            self.start_watching_btn.click()
        # TODO: add to check if not visible
