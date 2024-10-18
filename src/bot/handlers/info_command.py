"""This module handles the '/info' command for the Telegram bot. When triggered, 
it fetches and sanitizes information about the current Gemini model settings, 
such as the model name, temperature, top-p, top-k, and maximum output tokens, 
and sends it as a response message to the user. The message is formatted using 
MarkdownV2 for proper display in the Telegram chat.

Command:
    /info: Fetches and displays current Gemini model settings in a friendly, 
        formatted message.
"""
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from gemini import GeminiAPIClient, GeminiModelInfo
from utils import markdown_v2_sanitizer


CMD = "info"

async def handle_info_command(message: Message, bot: AsyncTeleBot) -> None:
    """
    Handle the '/info' command to display the current Gemini model settings.

    Args:
        message (Message): The incoming message from the user, containing 
            the '/info' command.
        bot (AsyncTeleBot): The asynchronous bot instance used to send responses.

    This function retrieves the model information using the GeminiAPIClient, 
    sanitizes it for safe display in a Telegram message using the 
    'markdown_v2_sanitizer', and sends the formatted response back to the 
    user's chat.

    Gemini Model Info:
        - Model Name: Name of the current model being used.
        - Temperature: Controls the randomness of the model's output.
        - Top P: The cumulative probability for selecting a subset of 
            possible tokens.
        - Top K: The number of highest probability tokens considered during 
            generation.
        - Max Output Tokens: The maximum number of tokens that the model can 
            generate.

    The message is sent using MarkdownV2 formatting for proper 
        display in Telegram.
    """

    model_info: GeminiModelInfo = GeminiAPIClient.get_model_info()

    model_info.model_name = markdown_v2_sanitizer.sanitize_code(
        model_info.model_name
        )
    model_info.top_p = markdown_v2_sanitizer.sanitize_float(
        model_info.top_p
        )
    model_info.temperature = markdown_v2_sanitizer.sanitize_float(
        model_info.temperature
        )
    
    response_message = (
        "Here's the scoop on my current settings\\! 🧠✨\n\n"
        f"\\- Model: `{model_info.model_name}` 🤖\n"
        f"\\- Temperature: *{model_info.temperature}* 🌡️ \\(spiciness level\\!\\)\n"
        f"\\- Top P: *{model_info.top_p}* 🎯 \\(sampling probability\\)\n"
        f"\\- Top K: *{model_info.top_k}* 🎰 \\(number of options considered\\)\n"
        f"\\- Max output tokens: *{model_info.max_output_tokens}* 🚀 \\(how much I can say in one go\\!\\)\n\n"
        "Tuned and ready for action\\! ⚡"
    )

    await bot.send_message(
        message.chat.id, 
        response_message, 
        parse_mode="markdownv2")