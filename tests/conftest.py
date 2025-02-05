import logging

import pytest

import config
from ui.pages.home_page import HomePage


@pytest.fixture
def twitch_home_page(chrome_mobile_driver) -> HomePage:
    logging.info("Open TwitchTV page")
    home_page = HomePage(chrome_mobile_driver)
    home_page.open_url(url=config.base_url)
    return home_page
