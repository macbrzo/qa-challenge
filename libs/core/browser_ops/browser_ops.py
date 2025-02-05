import logging
from datetime import datetime
from pathlib import Path


def take_screenshot(
    *,
    driver,
    test_name: str,
    screenshot_dir: str = "screenshots",
) -> None:
    """Helper function to capture and save a screenshot."""
    screenshot_dir = Path(screenshot_dir)
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{test_name}_{timestamp}.png"
    filepath = screenshot_dir / screenshot_name
    driver.save_screenshot(filepath)
    logging.info(f"Screenshot {screenshot_name} saved at {filepath}")
