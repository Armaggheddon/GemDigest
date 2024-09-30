import telebot
import url_checker
from settings import telegramKey

# Telegram api used:
#   - pip3 install pyTelegramBotAPI
#   - https://github.com/eternnoir/pyTelegramBotAPI

TELEGRAM_API_KEY = telegramKey.TELEGRAM_API_KEY
bot = telebot.TeleBot(TELEGRAM_API_KEY, parse_mode=None)

# Message handler to check if the message contains a URL
@bot.message_handler(func=lambda message: url_checker.contains_url(message.text))
def echo_all(message):
    # TODO:
    #   - Scrape the website (If is not a video from youtue)
    #   - Implement the google Gemini API to summarize the content
    #   - Return it to the user

    #? NOTE:
    #      If the content is a tweet? or a video from youtube? 
    #      or a twith with text and image/video?


    # Disable notification to avoid spamming the users (because if you send 
    # the message and the bot send the summary we have 2 notification and this 
    # is redundant for the same message)
    bot.reply_to(
        message,
        "URL detected: " + message.text,
        disable_notification=True
        )

# NOTE: If there is proble with infinity polling, you can use:
# bot.infinity_polling(timeout=10, long_polling_timeout = 5)
bot.infinity_polling()
