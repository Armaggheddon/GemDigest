"""This module initializes and runs the GemDigest Telegram bot using the 
    AsyncTeleBot from the telebot library. It registers custom filters and 
    handlers for various commands and messages, including /start, /tokens, 
    and links containing messages. The bot operates with asynchronous polling 
    to handle incoming messages.

Functions:
    register_custom_filters(bot: AsyncTeleBot) -> None:
        Registers custom filters for the bot to manage admin access and 
        link messages.

    register_handlers(bot: AsyncTeleBot) -> None:
        Registers message handlers for various commands and link messages.

    run() -> None:
        Initializes and starts the GemDigest bot with asynchronous polling.
"""
import asyncio
import logging

from telebot.async_telebot import AsyncTeleBot
from telebot import ExceptionHandler

from configs import api_keys
from utils import link_utils

from .handlers import (
    start_command,
    link_message,
    tokens_command,
    help_command,
    info_command
)

from . import filters


def register_custom_filters(bot: AsyncTeleBot) -> None:
    """Registers custom filters for the bot.

    This function adds filters to the bot for managing admin access 
    and link messages.

    Args:
        bot (AsyncTeleBot): The bot instance to which the filters are 
            being added.

    NOTE:
        The admin filter uses the admin user ID from the API keys 
        configuration.
    """
    bot.add_custom_filter(filters.AdminFilter(api_keys.get_admin_user_id()))
    bot.add_custom_filter(filters.LinkFilter())


def register_handlers(bot: AsyncTeleBot) -> None:
    """Registers message handlers for the GemDigest bot.

    This function sets up handlers for various types of messages that the bot 
    can receive. It registers a handler for the `/start` command and a 
    handler for processing text messages that contain URLs.

    Args:
        bot (AsyncTeleBot): The bot instance to which the handlers are 
            being registered.

    Handlers:
        - `/start` command: Calls `handle_start_command` when a user sends the 
            start command.
        - URL-containing messages: Calls `handle_link_message` when a text 
            message containing a URL is received.

    NOTE:
        The `pass_bot=True` argument is used to pass the bot instance to 
            the handler functions.
    """
    _filter_link = {filters.LinkFilter.key: True}
    _filter_admin = {filters.AdminFilter.key: True}

    _filter_link_admin = {**_filter_link, **_filter_admin}


    bot.register_message_handler(
        start_command.handle_start_command,
        commands=[start_command.CMD],
        pass_bot=True,
        **_filter_admin
    )

    bot.register_message_handler(
        link_message.handle_link_message,
        pass_bot=True,
        **_filter_link_admin
    )

    bot.register_message_handler(
        link_message.handle_no_link_message,
        pass_bot=True,
        **_filter_admin
    )

    bot.register_message_handler(
        tokens_command.handle_tokens_command,
        commands=[tokens_command.CMD],
        pass_bot=True,
        **_filter_admin
    )

    bot.register_message_handler(
        info_command.handle_info_command,
        commands=[info_command.CMD],
        pass_bot=True,
        **_filter_admin
    )

    bot.register_message_handler(
        help_command.handle_help_command,
        commands=[help_command.CMD],
        pass_bot=True,
        **_filter_admin
    )


def run() -> None:
    """Initializes and runs the GemDigest bot with asynchronous polling.

    This function creates an instance of the `AsyncTeleBot` class using the 
    Telegram bot token, registers the necessary handlers for bot operations, 
    and starts polling for messages asynchronously. The asyncio event could loop 
    runs with debug mode enabled, which provides detailed debugging information 
    (e.g., slow task detection, unawaited coroutines).

    NOTE:
        The bot is running with `debug=True`.
        Remove befor deploying the bot to production.
    """
    debug=False
    
    if debug:
        logging.warning("Debug Mode enabled for the bot asyncio runner.")

    gem_digest_bot = AsyncTeleBot(
        token = api_keys.get_telegram_api_key(),
        exception_handler=ExceptionHandler()
    )

    register_handlers(gem_digest_bot)
    register_custom_filters(gem_digest_bot)

    asyncio.run(gem_digest_bot.polling(), debug=debug)
