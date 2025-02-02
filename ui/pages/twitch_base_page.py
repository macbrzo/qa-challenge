from libs.core.ui import BaseElement, BasePage
from ui.pages.components.mobile_nav_bar import MobileNavBar


class TwitchTVPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.nav_bar = MobileNavBar(driver=driver)

        self.consent_banner_modal = BaseElement(
            driver=driver, locator="css=.consent-banner"
        )
        self.accept_btn = BaseElement(
            driver=driver, locator="css=button[data-a-target='consent-banner-accept']"
        )

    def accept_consent_banner_modal(self):
        if self.consent_banner_modal.is_present():
            self.accept_btn.click()

    def open_url(self, *, url: str):
        super().open_url(url=url)
        self.accept_consent_banner_modal()
