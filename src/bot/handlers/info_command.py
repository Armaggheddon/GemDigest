from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from gemini import GeminiAPIClient, GeminiModelInfo

CMD = "info"

async def handle_info_command(message: Message, bot: AsyncTeleBot) -> None:

    model_info = await GeminiAPIClient.get_model_info()

    info_message = (
        f"🚀 **Gemini Model Info** 🚀\n"
        f"Model Name: {model_info.model_name}\n"
        f"Temperature: {model_info.temperature}\n"
        f"Top P: {model_info.top_p}\n"
        f"Top K: {model_info.top_k}\n"
        f"Max Output Tokens: {model_info.max_output_tokens}\n"
    )

    await bot.send_message(message.chat.id, info_message)