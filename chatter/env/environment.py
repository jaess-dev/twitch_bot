import logging
from dotenv import load_dotenv
from os import getenv

load_dotenv()

LOGGER: logging.Logger = logging.getLogger("Bot")


class Variables(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Variables, cls).__new__(cls)
            cls.instance.init()

        return cls.instance

    def init(self):
        self.CLIENT_ID = getenv("TWITCH_CLIENT_ID")
        self.CLIENT_SECRET = getenv("TWITCH_CLIENT_SECRET")
        self.BOT_ID = getenv("SENDER_ID")
        self.OWNER_ID = getenv("BROADCASTER_ID")
