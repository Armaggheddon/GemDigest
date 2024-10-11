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
        "Here are the available commands 📒:\n"
        "/help - Display the list of available commands\n"
        "/tokens - Display the number of tokens used by the Gemini API\n"
        "message containing a URL - Extract and process URLs from the message\n" 
    )

    await bot.send_message(message.chat.id, help_message)