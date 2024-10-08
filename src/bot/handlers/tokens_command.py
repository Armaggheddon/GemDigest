from enum import Enum
from dataclasses import astuple

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from gemini import GeminiAPIClient

CMD = "tokens"

class Messages(Enum):
    TOKENS_TEMPLATE = (
        "Last input token count: {}\n"
        "Last output token count: {}\n"
        "Total input token count: {}\n"
        "Total output token count: {}\n"
        )
    
    def format(self, *args) -> str:
        return self.value.format(*args)
    

async def handle_tokens_command(message: Message, bot: AsyncTeleBot) -> None:
    
    token_count = GeminiAPIClient.get_used_tokens()
    response_message = Messages.TOKENS_TEMPLATE.format(
        *astuple(token_count)
    )

    await bot.send_message(message.chat.id, response_message)