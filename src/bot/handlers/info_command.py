from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from gemini import GeminiAPIClient, GeminiModelInfo
from utils import markdown_v2_sanitizer


CMD = "info"

async def handle_info_command(message: Message, bot: AsyncTeleBot) -> None:

    model_info: GeminiModelInfo = GeminiAPIClient.get_model_info()

    model_info.model_name = markdown_v2_sanitizer.sanitize_code(model_info.model_name)
    model_info.top_p = markdown_v2_sanitizer.sanitize_float(model_info.top_p)
    model_info.temperature = markdown_v2_sanitizer.sanitize_float(model_info.temperature)
    
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