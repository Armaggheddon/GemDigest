"""This module defines a custom filter for Telegram bot commands to 
    check if a message contains a URL. It uses the Telebot library 
    for implementing custom filters.

Classes:
    LinkFilter: A custom filter that checks if a message contains a URL.
"""
from telebot.types import Message
from telebot.asyncio_filters import SimpleCustomFilter

from utils import link_utils


class LinkFilter(SimpleCustomFilter):
    """Custom filter to check if a message contains a URL.

    This filter uses the `link_utils` module to determine whether the 
    message text includes a URL. It can be used to restrict certain 
    commands or functionalities based on the presence of a URL.

    Attributes:
        key (str): The key for the custom filter.

    Methods:
        check(message: Message, text: str) -> bool: Asynchronously checks 
        if the message text contains a URL.
    """
    key="has_url"

    @staticmethod
    async def check(message: Message) -> bool:
        """Checks if the provided message contains a URL.

        Args:
            message (Message): The message object to check.
            text (str): The text of the message to be evaluated.

        Returns:
            bool: `True` if the message text contains a URL, 
            `False` otherwise.
        """
        return True if link_utils.has_url(message.text) else False
