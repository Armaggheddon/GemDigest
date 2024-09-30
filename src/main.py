import asyncio

import telebot, telebot.types as types

from utils import url_checker
from utils import scraper
from settings import telegramKey


TELEGRAM_API_KEY = telegramKey.TELEGRAM_API_KEY
bot = telebot.TeleBot(TELEGRAM_API_KEY, parse_mode=None)

# Message handler to check if the message contains a URL
@bot.message_handler(func=lambda msg: url_checker.contains_url(msg.text))
def echo_all(message: types.Message):
    """
    """
    urls_content = []
    urls = url_checker.extract_urls(message.text)

    for url in urls:
        content = asyncio.run(scraper.scrape_website(url))
        urls_content.append(content)

    print(urls_content)
    # bot.reply_to(
    #     message,
    #     "URL detected: " + urls_content,
    #     disable_notification=True
    #     )

if __name__ == "__main__":
    bot.infinity_polling()
