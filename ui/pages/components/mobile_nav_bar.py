from libs.core.ui import BaseElement


class MobileNavBar:
    def __init__(self, driver, parent_locator: str = "css=div.dShAUu", logger=None):
        self.driver = driver
        self.parent_locator = BaseElement(driver, locator=parent_locator)
        self.search_btn = BaseElement(
            driver, parent=self.parent_locator, locator="css=[href='/directory']"
        )
        self.logger = logger

    def navigate_to_search_page(self):
        self.search_btn.click()
        from ui.pages.browse_page import BrowsePage

        search_page = BrowsePage(driver=self.driver)
        search_page.wait_for_page_to_load()
        return search_page
