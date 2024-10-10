from telebot.types import Message
from telebot.asyncio_filters import SimpleCustomFilter

class AdminFilter(SimpleCustomFilter):

    key: str = "admin_filter"
    admin_user_id: int = 0

    def __init__(self, admin_user_id: int):
        AdminFilter.admin_user_id = admin_user_id

    @staticmethod
    async def check(message: Message) -> bool:
        return message.from_user.id == AdminFilter.admin_user_id