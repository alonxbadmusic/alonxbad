import time
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

from config import START_IMG_URL, SUPPORT_GROUP, LOG_GROUP_ID, BANNED_USERS
from Aloxbad import app
from Aloxbad.misc import _boot_
from Aloxbad.plugins.sudo.sudoers import sudoers_list
from Aloxbad.utils.database import (
    add_served_chat, add_served_user, blacklisted_chats,
    get_lang, is_banned_user, is_on_off,
)
from Aloxbad.utils import bot_sys_stats
from Aloxbad.utils.decorators.language import LanguageStart
from Aloxbad.utils.formatters import get_readable_time
from Aloxbad.utils.inline import help_pannel, private_panel, start_panel
from strings import get_string


@app.on_message(filters.command("start") & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_private(client, message: Message, _):
    await add_served_user(message.from_user.id)
    args = message.text.split()

    if len(args) > 1:
        param = args[1]

        if param.startswith("help"):
            return await message.reply_photo(
                photo=START_IMG_URL,
                caption=_["help_1"].format(SUPPORT_GROUP),
                reply_markup=help_pannel(_),
            )

        elif param.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                await app.send_message(
                    LOG_GROUP_ID,
                    f"{message.from_user.mention} opened sudo panel.\nID: <code>{message.from_user.id}</code>",
                )
            return

        elif param.startswith("inf"):
            m = await message.reply_text("🔎 Searching...")
            query = param.replace("info_", "", 1)
            results = await VideosSearch(f"https://www.youtube.com/watch?v={query}", limit=1).next()
            for result in results["result"]:
                searched_text = _["start_6"].format(
                    result["title"],
                    result["duration"],
                    result["viewCount"]["short"],
                    result["publishedTime"],
                    result["channel"]["link"],
                    result["channel"]["name"],
                    app.mention,
                )
                buttons = InlineKeyboardMarkup([
                    [InlineKeyboardButton(_["S_B_8"], url=result["link"])],
                    [InlineKeyboardButton(_["S_B_9"], url=SUPPORT_GROUP)]
                ])
                await m.delete()
                return await message.reply_photo(
                    photo=result["thumbnails"][0]["url"].split("?")[0],
                    caption=searched_text,
                    reply_markup=buttons
                )

            if await is_on_off(2):
                await app.send_message(
                    LOG_GROUP_ID,
                    f"{message.from_user.mention} checked track info.\nID: <code>{message.from_user.id}</code>",
                )
            return

    out = private_panel(_)
    UP, CPU, RAM, DISK = await bot_sys_stats()
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["start_2"].format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM),
        reply_markup=InlineKeyboardMarkup(out),
    )
    if await is_on_off(2):
        await app.send_message(
            LOG_GROUP_ID,
            f"{message.from_user.mention} started the bot.\nID: <code>{message.from_user.id}</code>",
        )


@app.on_message(filters.command("start") & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_group(client, message: Message, _):
    await add_served_chat(message.chat.id)
    uptime = get_readable_time(int(time.time() - _boot_))
    out = start_panel(_)
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["start_1"].format(app.mention, uptime),
        reply_markup=InlineKeyboardMarkup(out),
    )


@app.on_message(filters.new_chat_members, group=-1)
async def new_member_joined(client, message: Message):
    for member in message.new_chat_members:
        try:
            _ = get_string(await get_lang(message.chat.id))

            if await is_banned_user(member.id):
                await message.chat.ban_member(member.id)
                continue

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            SUPPORT_GROUP,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                await add_served_chat(message.chat.id)
                await message.reply_photo(
                    photo=START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(start_panel(_)),
                )
                await message.stop_propagation()

        except Exception:
            pass
