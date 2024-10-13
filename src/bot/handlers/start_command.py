"""This module contains the implementation for handling the /start command in a 
    Telegram bot. It includes an enumeration for message templates and an 
    asynchronous function to process the /start command, sending a welcome message 
    to the user.

Classes:
    Messages: An enumeration class for defining template messages used by the bot.

Functions:
    handle_start_command(message: Message, bot: AsyncTeleBot) -> None:
        Handles the /start command by sending a personalized welcome message 
            to the user.
"""
from enum import Enum

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


CMD = 'start'

async def handle_start_command(message: Message, bot: AsyncTeleBot) -> None:
    """Handles the /start command for the bot.

    This asynchronous function sends a welcome message to the user who initiates 
    the `/start` command. The message is personalized with the user's first name.

    Args:
        message (Message): The message object representing the 
            incoming /start command.
        bot (AsyncTeleBot): The instance of the bot used to send the 
            response message.

    Returns:
        None: This function does not return a value.

    Example:
        User sends `/start`, and the bot replies with a personalized 
            welcome message.

    """

    start_message = (
        f"Hey {message.from_user.first_name}\\!👋\n"
        "I'm *GemDigest*, your friendly bot 🤖, here to help you summarize "
        "links, articles, and more\\! 🔗✨ "
        "Just send a link or use /help to see all the cool things "
        "I can do\\! \n"
        "Let's get started\\! 🚀")

    await bot.send_message(
        message.chat.id,
        start_message,
        parse_mode='markdownv2'
    )