import json

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def formatter(raw_str: str) -> tuple[bool, str]:
    """
    """
    raw_json = json.loads(raw_str)

    try:
        title = title_builder(raw_json["title"])
        summary = summary_builder(raw_json["summary"])
        image = image_builder(raw_json["url"])

    except TypeError as e:
        # Log the error or return a default message
        print(f"Error processing raw_json: {raw_json}, error: {e}")
        return (False, "Error: Invalid data format.")
    
    return (True, f"<b>{title}</b>\n\n{summary}\n<a href='{image}'>&#8205</a>")


def title_builder(title: str) -> str:
    """
    TODO:
    """
    return title


def summary_builder(summary: str) -> str:
    """
    TODO:
    """
    return summary


def image_builder(image_url: str) -> str:
    """
    TODO:
    """
    return image_url.rstrip("/|\\")


def gen_markup(button_link: str) -> InlineKeyboardMarkup:
    """
    """
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("📄 READ THE ARTICLE", 
                             callback_data="article",
                             url=button_link),

        # InlineKeyboardButton("SECOND BUTTON", 
        #                      callback_data="apri app", 
        #                      url=button_link)
        )
    return markup