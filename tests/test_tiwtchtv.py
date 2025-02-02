from ui.pages.components.streamer_channel import StreamerChannel


def test_navigate_to_streamer(twitch_home_page):
    page = twitch_home_page.nav_bar.navigate_to_search_page()
    page.search_twitch("StarCraft II")
    page.navigate_to_channels()
    page.scroll_by_screen(screens_count=2)
    visible_channels = page.list_visible_channels()
    visible_channels[2].click()
    # page = twitch_home_page
    # twitch_home_page.open_url(url="https://m.twitch.tv/protech")
    stream = StreamerChannel(page.driver)
    stream.handle_content_gate_popup()
    stream.wait_for_video_to_play()
