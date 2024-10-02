import asyncio
import collections

import telebot, telebot.types as types

import settings
from utils import url_checker
from utils import scraper
from utils import google_gemini as gemini
from utils import toolkit

# TODO: Fix the prompt such that the output is whell formatted in html for telegram

TELEGRAM_API_KEY = settings.TELEGRAM_API_KEY
bot = telebot.TeleBot(TELEGRAM_API_KEY, parse_mode=None)

# Message handler to check if the message contains a URL
@bot.message_handler(func=lambda msg: url_checker.contains_url(msg.text))
def echo_all(message: types.Message):
    """
    """
    content_element = collections.namedtuple(
        "ContentElement", 
        ("content", "sub_urls", "original_url")
        )
    
    urls_content = []
    urls = url_checker.extract_urls(message.text)

    for url in urls:
        content = asyncio.run(scraper.scrape_website(url))
        sub_urls = url_checker.extract_urls(content)

        element = content_element(
            content=content, 
            sub_urls=sub_urls,
            original_url=url
            )
        
        urls_content.append(element)

    for element in urls_content:
        prompt = element.content + "\n\n" + "\n".join(element.sub_urls)
        print(prompt, "\n\n\n\n")
        output = gemini.generate_text(settings.generation_config, prompt)
    
        print(output)
        message_replay = toolkit.formatter(output)

        if message_replay[0]:
            bot.reply_to(
                message,
                message_replay[1],
                disable_notification=True,
                parse_mode = 'html', 
                reply_markup=toolkit.gen_markup(element.original_url)
                )

if __name__ == "__main__":
    bot.infinity_polling()
