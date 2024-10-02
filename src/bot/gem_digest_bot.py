import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot import ExceptionHandler

from configs import api_keys

from .handlers import start_command
from .handlers import link_message
from . import filters
from . import utils

def register_custom_filters(bot: AsyncTeleBot) -> None:
    bot.add_custom_filter(filters.LinkFilter())

def register_handlers(bot: AsyncTeleBot) -> None:
    bot.register_message_handler(
        start_command.handle_start_command,
        commands=[start_command.CMD],
        pass_bot=True
    )

    bot.register_message_handler(
        link_message.handle_link_message,
        content_types=['text'],
        func=lambda msg: utils.has_url(msg.text),
        pass_bot=True
    )


def run() -> None:
    
    gem_digest_bot = AsyncTeleBot(
        token = api_keys.TELEGRAM_BOT_TOKEN, 
        exception_handler=ExceptionHandler()
    )

    #register_custom_filters(gem_digest_bot)
    register_handlers(gem_digest_bot)

    asyncio.run(gem_digest_bot.polling())