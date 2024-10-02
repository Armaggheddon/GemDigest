from enum import Enum
import collections

from crawl4ai import AsyncWebCrawler
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from gemini import gemini_api
from .. import utils


class Messages(Enum):
    START_TEMPLATE = ("""
        Hello %(user_name)! I'm a bot that can generate text based on your prompt.
        Just send me a message with your prompt and I'll generate a response for you.
        """)
    
    def format(self, *args, **kwargs) -> str:
        return self.value % kwargs



async def handle_link_message(message: Message, bot: AsyncTeleBot):
    
    content_element = collections.namedtuple(
        "ContentElement", 
        ("content", "sub_urls", "original_url")
    )
    urls_content = []
    urls = utils.extract_urls(message.text)

    # TODO: use here or inside the gemini_api?
    async with AsyncWebCrawler(verbose=True) as scraper:
        for url in urls:
            content = (await scraper.arun(url=url)).markdown
            sub_urls = utils.extract_urls(content)

            element = content_element(
                content=content, 
                sub_urls=sub_urls,
                original_url=url
            )

            urls_content.append(element)
    
    for element in urls_content:
        prompt = element.content + "\n\n" + "\n".join(element.sub_urls)
        print(prompt, "\n\n\n\n")
        output = await gemini_api.generate_text(prompt)

        await bot.reply_to(
            message,
            output,
            disable_notification=True,
            parse_mode='html',
            reply_markup=utils.gen_markup(element.original_url)
        )