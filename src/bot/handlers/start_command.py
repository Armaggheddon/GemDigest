from enum import Enum

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


CMD = 'start'

class Messages(Enum):
    """An enumeration class that contains template messages used by the bot.

    This class defines various message templates for different bot responses. 
    The `START_TEMPLATE` is a welcome message template that can be personalized 
    with a user's name. The `format` method allows for dynamic content insertion 
    into the message templates using string formatting.

    Attributes:
        START_TEMPLATE (str): A template message sent when a user starts 
            interacting with the bot, personalized with the user's first name.

    Methods:
        format(*args, **kwargs) -> str:
            Formats the message template with the provided keyword arguments.
            This is used to inject dynamic content (e.g., user names) into the 
            message template.
    """
    START_TEMPLATE = ("""
        Hello %(user_name)! I'm a bot that can generate text based on your prompt.
        Just send me a message with your prompt and I'll generate a response for you.
        """)
    
    def format(self, *args, **kwargs) -> str:
        """Formats the message template with the given keyword arguments.

        Args:
            *args: Additional positional arguments (not used in this method).
            **kwargs: Keyword arguments used for formatting the message template. 
                      For example, `user_name` can be passed to personalize the 
                      START_TEMPLATE message.

        Returns:
            str: The formatted message with the dynamic content inserted.

        Example:
            formatted_message = Messages.START_TEMPLATE.format(user_name="John")
        """
        return self.value % kwargs


async def handle_start_command(message: Message, bot: AsyncTeleBot) -> None:
    """Handles the /start command for the bot.

    This asynchronous function sends a welcome message to the user who initiates 
    the `/start` command. The message is personalized with the user's first name.

    Args:
        message (Message): The message object representing the 
            incoming /start command.
        bot (AsyncTeleBot): The instance of the bot used to send the 
            response message.

    Returns:
        None: This function does not return a value.

    Example:
        User sends `/start`, and the bot replies with a personalized 
            welcome message.

    """
    await bot.send_message(
        message.chat.id,
        Messages.START_TEMPLATE.format(user_name=message.from_user.first_name)
    )