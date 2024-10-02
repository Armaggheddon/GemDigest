from enum import Enum
import re
import collections

from crawl4ai import AsyncWebCrawler
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from utils import toolkit
from gemini_manager import gemini_api


class Messages(Enum):
    START_TEMPLATE = ("""
        Hello %(user_name)! I'm a bot that can generate text based on your prompt.
        Just send me a message with your prompt and I'll generate a response for you.
        """)
    
    def format(self, *args, **kwargs):
        return self.value % kwargs


regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

def contains_url(text: str) -> bool:
    """
    """
    # Ho fatto un esame sulle regex ma sicuro chatgpt le fa meglio di me
    url_pattern = re.compile(regex)
    
    if url_pattern.search(text):
        return True
    else:
        return False


def extract_urls(text: str) -> list[str]:
    """
    """
    urls_list = []
    
    url_pattern = re.compile(regex)
    urls = url_pattern.findall(text)

    for url in urls:
        urls_list.append(url[0])

    return urls_list


async def handle_link_message(message: Message, bot: AsyncTeleBot):
    
    content_element = collections.namedtuple(
        "ContentElement", 
        ("content", "sub_urls", "original_url")
    )
    urls_content = []
    urls = extract_urls(message.text)

    async with AsyncWebCrawler(verbose=True) as scraper:
        for url in urls:
            content = (await scraper.arun(url=url)).markdown
            sub_urls = extract_urls(content)

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

        is_success, reply = toolkit.formatter(output)

        if is_success:
            await bot.reply_to(
                message,
                reply,
                disable_notification=True,
                parse_mode='html',
                reply_markup=toolkit.gen_markup(element.original_url)
            )