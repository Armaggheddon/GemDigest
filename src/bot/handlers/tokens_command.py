"""This module contains the implementation for handling the /tokens command in 
    a Telegram bot. It an asynchronous function to process the /tokens command,
    sending the token counts to the user.

Functions:
    handle_tokens_command(message: Message, bot: AsyncTeleBot) -> None:
        Handles the /tokens command by sending the token usage statistics 
        to the user.
"""
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from gemini import GeminiAPIClient


CMD = "tokens"    

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
    # response_message = message_template % astuple(token_count)
    total_tokens_used = (token_count.total_input_token_count 
        + token_count.total_output_token_count)
    
    response_message = (
        "Here's the token breakdown\\! 🧮✨\n\n"
        f"\\- Last input: *{token_count.last_input_token_count}* tokens 📝\n"
        f"\\- Last output: *{token_count.last_output_token_count}* tokens 🗣️\n"
        f"\\- Total input: *{token_count.total_input_token_count}* tokens 💻\n"
        f"\\- Total output: *{token_count.total_output_token_count}* tokens 🔊\n"
        f"\\- Total tokens used: *{total_tokens_used}* tokens 🚀\n"
    )

    await bot.send_message(
        message.chat.id, 
        response_message, 
        parse_mode="markdownv2")