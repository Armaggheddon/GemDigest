"""This module defines a custom filter for Telegram bot commands 
    to restrict access to admin users only. It uses the Telebot library 
    for implementing filters.

Classes:
    AdminFilter: A custom filter that checks if the user is an admin.
"""
from typing import Union, List

from telebot.types import Message
from telebot.asyncio_filters import SimpleCustomFilter


class AdminFilter(SimpleCustomFilter):
    """Custom filter to allow access only to admin users.

    This filter checks whether the user who sent the message 
    matches the admin user ID. It is designed to restrict certain 
    commands or functionalities to the designated admin user.

    Attributes:
        key (str): The key for the custom filter.
        admin_user_id (int): The ID of the admin user.

    Methods:
        check(message: Message) -> bool: Asynchronously checks if the 
        user ID of the message sender matches the admin user ID.
    """
    key: str = "admin_filter"
    admin_user_ids: List[int] = 0

    def __init__(self, admin_user_id: Union[int, List[int]]):
        """Initializes the AdminFilter with the admin user ID.

        Args:
            admin_user_id (int): The user ID of the admin.
        """
        if isinstance(admin_user_id, int):
            admin_user_id = [admin_user_id]
        AdminFilter.admin_user_ids = admin_user_id

    @staticmethod
    async def check(message: Message) -> bool:
        """Checks if the sender of the message is the admin user.

        Args:
            message (Message): The message object to check.

        Returns:
            bool: `True` if the sender is the admin user, `False` otherwise.
        """
        return message.from_user.id in AdminFilter.admin_user_ids