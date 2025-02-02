import pytest

from ui.pages.home_page import HomePage


@pytest.fixture
def twitch_home_page(driver) -> HomePage:
    home_page = HomePage(driver)
    home_page.open_url(url="https://www.twitch.tv/")
    return home_page
