from enum import Enum
from typing import List

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from crawler import crawl_urls, ScrapeResult
from gemini import gemini_api_client
from utils import link_utils

from ..bot_utils import message_markup


class Messages(Enum):
    START_TEMPLATE = ("""
        Hello %(user_name)! I'm a bot that can generate text based on your prompt.
        Just send me a message with your prompt and I'll generate a response for you.
        """)
    
    def format(self, *args, **kwargs) -> str:
        return self.value % kwargs
    

async def handle_link_message(message: Message, bot: AsyncTeleBot):

    urls = link_utils.extract_urls(message.text)
            
    scrape_results: List[ScrapeResult] = await crawl_urls(urls)
    
    for result in scrape_results:
        prompt = result.content + "\n\n" + "\n".join(result.sub_urls)
        output = await gemini_api_client.generate_text(prompt)

        await bot.reply_to(
            message,
            output,
            disable_notification=True,
            parse_mode='html',
            reply_markup=message_markup.generate_article_button_markup(result.original_url)
        )