from telebot.types import Message
from telebot.asyncio_filters import AdvancedCustomFilter

from utils import link_utils

class LinkFilter(AdvancedCustomFilter):
    key="has_url"

    @staticmethod
    async def check(message: Message, text: str) -> bool:
        return True if link_utils.has_url(message.text) else False
