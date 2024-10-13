"""This module contains the handler for the /help command in a Telegram bot. 
    When a user invokes the /help command, it sends a message listing the 
    available commands to the user.

Functions:
    handle_help_command(message: Message, bot: AsyncTeleBot) -> None: 
    Handles the /help command by sending a list of available commands to 
    the user.
"""
from enum import Enum

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

CMD = "help"

async def handle_help_command(message: Message, bot: AsyncTeleBot) -> None:
    """Handles the /help command by sending a list of available commands to the user.

    Args:
        message (Message): The message object that triggered the command.
        bot (AsyncTeleBot): The bot instance used to send the response.
    """
    help_message = (
        "👋 Hey there\\!\n" 
        "🤖 Here's what I can do for you:\n\n"
        "\\-/help : You're already here\\! 📚\n\n"
        "\\- /tokens : I'll show you how many tokens we've crunched through so far\\! 📊\n\n"
        "\\- /info : Check out the current Gemini model settings I'm running on\\! 🧠✨\n\n"
        "\\- Just send me a message with one or more links\\!\n\n"
        "I'll fetch the goods and summarize it for you\\! 🔗📋\n"
        "Need anything else\\? Just ask\\! 😎"
    )

    await bot.send_message(
        message.chat.id, 
        help_message, 
        parse_mode="markdownv2")