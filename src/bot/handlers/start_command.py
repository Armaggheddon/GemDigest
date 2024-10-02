from enum import Enum

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


CMD = 'start'

class Messages(Enum):
    START_TEMPLATE = ("""
        Hello %(user_name)! I'm a bot that can generate text based on your prompt.
        Just send me a message with your prompt and I'll generate a response for you.
        """)
    
    def format(self, *args, **kwargs):
        return self.value % kwargs



async def handle_start_command(message: Message, bot: AsyncTeleBot):
    await bot.send_message(
        message.chat.id,
        Messages.START_TEMPLATE.format(user_name=message.from_user.first_name)
    )