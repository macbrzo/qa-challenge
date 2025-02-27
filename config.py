from os import getenv

from dotenv import load_dotenv

load_dotenv()

base_url = getenv("BASE_URL", "https://www.twitch.tv/")
global_timeout = getenv("GLOBAL_TIMEOUT", 10)
remote_url = getenv("REMOTE_URL")
