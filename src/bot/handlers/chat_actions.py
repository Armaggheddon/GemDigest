from telebot.types import ChatMemberUpdated
from telebot.async_telebot import AsyncTeleBot

from configs import api_keys

_admin_ids = api_keys.get_admin_user_ids()

async def handle_chat_join(
    chat_member_updated: ChatMemberUpdated, 
    bot: AsyncTeleBot
) -> None:
    """ Handle the bot joining a chat.
    """
    added_by_user_id = chat_member_updated.from_user.id

    if not added_by_user_id in _admin_ids:
        # Leave the chat if the bot was not added by an admin
        return await bot.leave_chat(chat_member_updated.chat.id)

    chat_join_message = (
        "👋 Hey everyone\\!\n"
        "I'm *GemDigest* 🤖, your handy bot for turning long articles "
        "into bite\\-sized summaries\\. Just share a link to an article, "
        "and I'll bring you the highlights in no time\\! 📰✨\n\n"
        "Need more info? Type /help to see all the ways I can assist you\\. "
        "Let me help you save time and get straight to the point\\. 🎯\n"
        "Drop a link, and let's get started\\! 📝🔗"
    )

    # is one of "member", "administrator" or "left"
    bot_status = chat_member_updated.new_chat_member.status
    chat_member_updated.new_chat_member.status

    if bot_status == "member":
        await bot.send_message(
            chat_member_updated.chat.id,
            chat_join_message,
            parse_mode="markdownv2",
            disable_notification=True
        )

    # TODO: uncomment for testing so that bot automatically leaves chat
    # await bot.leave_chat(chat_member_updated.chat.id)


async def handle_member_joined(
    chat_member_updated: ChatMemberUpdated, 
    bot: AsyncTeleBot
) -> None:
    # TODO: is never called, why??
    print("chat_member_updated: ", chat_member_updated)
    with open("chat_member_updated.txt", "w") as f:
        f.write(str(chat_member_updated))

    user_name = chat_member_updated.new_chat_member.user.username

    chat_join_message = (
        f"👋 Welcome, {user_name}\\!\n"
        "I'm GemDigest, the bot here to help you stay on top "
        "of the latest articles without all the reading\\! 📚✨ "
        "Just share a link, and I'll send you a quick summary\\.\n\n"
        "Need more info? Type /help to see all the ways I can assist you\\. "
        "Looking forward to saving you some time\\! "
        "Drop a link anytime you want the scoop\\. 📰🔗"
    )

    await bot.send_message(
        chat_member_updated.chat.id,
        chat_join_message,
        parse_mode="markdownv2",
        disable_notification=True
    )
    