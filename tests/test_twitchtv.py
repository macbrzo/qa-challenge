import logging

from ui.pages.components.streamer_channel import StreamerChannel


def test__success__stream_started(twitch_home_page):
    """
    Verifies if stream starts for 2nd streamer on Channels list after scrolling two screens

    || Test Scenario ||
    | 1. Using NavBar navigate to search page |
    | 2. Search for StarCraft II |
    | 3. Navigate to channels |
    | 4. Scroll two screens |
    | 5. Select 2nd visible LIVE stream |
    | 6. Handle Pop-up |
    | 7. Verify Stream started |
    """
    logging.info("1. Using NavBar navigate to search page")
    ttv_page = twitch_home_page.nav_bar.navigate_to_search_page()

    logging.info("2. Search for StarCraft II")
    ttv_page.search_twitch("StarCraft II")

    logging.info("3. Navigate to channels")
    ttv_page.navigate_to_channels()

    logging.info("4. Scroll two screens")
    ttv_page.scroll_by_screen(screens_count=2)

    logging.info("5. Select 2nd visible LIVE stream")
    visible_channels = ttv_page.list_visible_channels()
    visible_channels[1].click()

    logging.info("6. Handle Pop-up")
    stream = StreamerChannel(ttv_page.driver)
    stream.handle_content_gate_popup()

    logging.info("7. Verify Stream started")
    assert stream.is_video_started()
