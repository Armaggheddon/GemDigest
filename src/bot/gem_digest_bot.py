import asyncio

from telebot.async_telebot import AsyncTeleBot

from .handlers import start_command
from .handlers import link_message
from configs import api_keys


def register_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(
        start_command.handle_start_command,
        commands=[start_command.CMD],
        pass_bot=True
    )

    bot.register_message_handler(
        link_message.handle_link_message,
        content_types=['text'],
        func=lambda msg: link_message.contains_url(msg.text),
        pass_bot=True
    )


def run():
    
    gem_digest_bot = AsyncTeleBot(token = api_keys.TELEGRAM_BOT_TOKEN)

    register_handlers(gem_digest_bot)

    asyncio.run(gem_digest_bot.polling())