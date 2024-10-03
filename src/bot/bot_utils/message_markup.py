from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_article_button_markup(button_link: str) -> InlineKeyboardMarkup:
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