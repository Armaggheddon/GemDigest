"""This module provides functionality to create Telegram inline keyboard 
    markups for interacting with users. It includes a function to generate 
    an inline button that links to an article.

Functions:
    generate_article_button_markup: Generates an inline keyboard markup 
    with a button linking to the article.
"""
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_article_button_markup(button_link: str) -> InlineKeyboardMarkup:
    """Generates an inline keyboard markup with a button linking to the article.

    This function creates a Telegram inline keyboard with a single button 
    labeled "📄 READ THE ARTICLE". When clicked, the button directs the user 
    to the provided URL (`button_link`).

    Args:
        button_link (str): The URL to which the button should redirect.

    Returns:
        InlineKeyboardMarkup: A markup object that contains the inline button 
        linked to the provided URL.

    Example:
        generate_article_button_markup("http://example.com/article")
    """
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton(
            "📄 READ THE ARTICLE", 
            callback_data="article",
            url=button_link
        ),
    )
    return markup