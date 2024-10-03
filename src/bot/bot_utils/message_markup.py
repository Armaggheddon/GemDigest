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
        InlineKeyboardButton("📄 READ THE ARTICLE", 
                             callback_data="article",
                             url=button_link),

        # InlineKeyboardButton("SECOND BUTTON", 
        #                      callback_data="apri app", 
        #                      url=button_link)
        )
    return markup