import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot import ExceptionHandler

from configs import APIKeys
from utils import link_utils

from .handlers import start_command
from .handlers import link_message
from .filters.links_filter import LinkFilter

def register_custom_filters(bot: AsyncTeleBot) -> None:
    bot.add_custom_filter(LinkFilter())

def register_handlers(bot: AsyncTeleBot) -> None:
    bot.register_message_handler(
        start_command.handle_start_command,
        commands=[start_command.CMD],
        pass_bot=True
    )

    bot.register_message_handler(
        link_message.handle_link_message,
        content_types=['text'],
        func=lambda msg: link_utils.has_url(msg.text),
        pass_bot=True
    )


def run() -> None:
    
    gem_digest_bot = AsyncTeleBot(
        token = APIKeys.TELEGRAM_BOT_TOKEN, 
        exception_handler=ExceptionHandler()
    )

    #register_custom_filters(gem_digest_bot)
    register_handlers(gem_digest_bot)

    asyncio.run(gem_digest_bot.polling(), debug=True)