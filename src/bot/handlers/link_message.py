"""This module contains the implementation for handling messages that contain 
    URLs in a Telegram bot. It includes an enumeration for message templates 
    and an asynchronous function to process incoming messages, extract URLs, 
    crawl them for content, and respond to the user with generated text and 
    links to articles.

Classes:
    Messages: An enumeration class for defining template messages used by the bot.

Functions:
    handle_link_message(message: Message, bot: AsyncTeleBot) -> None:
        Handles messages containing URLs by extracting and processing the links.
"""
from enum import Enum
from typing import List

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from crawler import crawl_urls, ScrapeResult
from gemini import GeminiAPIClient, GeminiResponse
from utils import link_utils

from ..bot_utils import message_markup


class Messages(Enum):
    """An enumeration class that contains template messages used by the bot.

    This class defines various message templates for different bot responses. 
    The `START_TEMPLATE` is a welcome message template that can be personalized 
    with a user's name. The `format` method allows for dynamic content insertion 
    into the message templates using string formatting.

    Attributes:
        START_TEMPLATE (str): A template message sent when a user starts 
            interacting with the bot, personalized with the user's first name.

    Methods:
        format(*args, **kwargs) -> str:
            Formats the message template with the provided keyword arguments.
            This is used to inject dynamic content (e.g., user names) into the 
            message template.
    """
    START_TEMPLATE = ("""
        Hello %(user_name)! I'm a bot that can generate text based on your prompt.
        Just send me a message with your prompt and I'll generate a response for you.
        """)
    
    def format(self, *args, **kwargs) -> str:
        """Formats the message template with the given keyword arguments.

        Args:
            *args: Additional positional arguments (not used in this method).
            **kwargs: Keyword arguments used for formatting the message template. 
                      For example, `user_name` can be passed to personalize the 
                      START_TEMPLATE message.

        Returns:
            str: The formatted message with the dynamic content inserted.

        Example:
            formatted_message = Messages.START_TEMPLATE.format(user_name="John")
        """
        return self.value % kwargs
    

async def handle_link_message(message: Message, bot: AsyncTeleBot) -> None:
    """Handles messages containing URLs by extracting and processing the links.

    This asynchronous function performs the following tasks:
        1. Extracts URLs from the incoming text message.
        2. Crawls the extracted URLs to scrape their content and sub-links.
        3. Generates a text response based on the scraped content using 
            the Gemini API.
        4. Replies to the user with the generated text, including a button 
            linking to the original article.

    Args:
        message (Message): The incoming Telegram message containing the URLs.
        bot (AsyncTeleBot): The bot instance used to send the reply message.

    Returns:
        None: This function does not return a value.
    """
    urls = link_utils.extract_urls(message.text)
            
    scrape_results: List[ScrapeResult] = await crawl_urls(urls)
    
    for result in scrape_results:
        prompt = result.content + "\n\n" + "\n".join(result.sub_urls)
        output: GeminiResponse = await GeminiAPIClient.generate_text(prompt)

        # TODO: add error_message formatting

        await bot.reply_to(
            message,
            output.text if output.text else output.error_message,
            disable_notification=True,
            parse_mode='html',
            reply_markup=message_markup.generate_article_button_markup(
                result.original_url
                )
        )