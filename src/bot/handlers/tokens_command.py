"""This module contains the implementation for handling the /tokens command in 
    a Telegram bot. It includes an enumeration for message templates and an 
    asynchronous function to process the /tokens command, sending the token 
    counts to the user.

Classes:
    Messages: An enumeration class for defining message templates used by the bot.

Functions:
    handle_tokens_command(message: Message, bot: AsyncTeleBot) -> None:
        Handles the /tokens command by sending the token usage statistics 
            to the user.
"""
from enum import Enum
from dataclasses import astuple

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from gemini import GeminiAPIClient

CMD = "tokens"


class Messages(Enum):
    """An enumeration class that contains template messages used by the bot.

    This class defines various message templates for different bot responses. 
    The `TOKENS_TEMPLATE` is a message template used to display token counts.

    Attributes:
        TOKENS_TEMPLATE (str): A template message displaying various 
            token counts.

    Methods:
        format(*args) -> str:
            Formats the message template with the provided arguments for 
                token counts.
    """
    TOKENS_TEMPLATE = (
        "Last input token count: {}\n"
        "Last output token count: {}\n"
        "Total input token count: {}\n"
        "Total output token count: {}\n"
        )
    
    def format(self, *args) -> str:
        """Formats the message template with the provided arguments.

        Args:
            *args: Arguments used for formatting the message template.

        Returns:
            str: The formatted message with the token counts inserted.

        Example:
            formatted_message = Messages.TOKENS_TEMPLATE.format(10, 20, 100, 200)
        """
        return self.value.format(*args)
    

async def handle_tokens_command(message: Message, bot: AsyncTeleBot) -> None:
    """Handles the /tokens command for the bot.

    This asynchronous function retrieves the token usage statistics from the 
    GeminiAPIClient and sends a formatted message containing the token counts 
    to the user who initiated the command.

    Args:
        message (Message): The message object representing the 
            incoming /tokens command.
        bot (AsyncTeleBot): The instance of the bot used to send the 
            response message.

    Returns:
        None: This function does not return a value.

    Example:
        User sends `/tokens`, and the bot replies with the token usage 
            statistics.
    """
    token_count = GeminiAPIClient.get_used_tokens()
    response_message = Messages.TOKENS_TEMPLATE.format(
        *astuple(token_count)
    )

    await bot.send_message(message.chat.id, response_message)