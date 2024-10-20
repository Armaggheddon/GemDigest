from telebot.types import Message
from telebot.asyncio_filters import SimpleCustomFilter


class PrivateChatFilter(SimpleCustomFilter):
    """
    Filters messages that are from a private chat, i.e.
    the message.chat.type field is NOT one of the following
    “group”, “supergroup” or “channel”.

    if message.chat.type == "private" returns True
    if message.chat.type in ["group", "supergroup", "channel"] returns False


    """
    
    key="private_chat"

    @staticmethod
    async def check(message: Message) -> bool:
        """Checks if the message is from a private chat, i.e. with a single user.
        """
        return True if message.chat.type == "private" else False
