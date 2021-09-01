# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ Commands Available -

• `{i}mute <reply to msg/ user id>`
    Mute user in current chat.

• `{i}unmute <reply to msg/ user id>`
    Unmute user in current chat.

• `{i}dmute <reply to msg/ user id>`
    Mute user in current chat by deleting msgs.

• `{i}undmute <reply to msg/ use id>`
    Unmute dmuted user in current chat.

• `{i}tmute <time> <reply to msg/ use id>`
    s- seconds
    m- minutes
    h- hours
    d- days
    Mute user in current chat with time.
"""
from pyUltroid.functions.all import ban_time
from pyUltroid.functions.mute_db import is_muted, mute, unmute
from telethon import events

from . import *


@ultroid_bot.on(events.NewMessage(incoming=True))
async def watcher(event):
    if is_muted(f"{event.sender_id}_{event.chat_id}"):
        await event.delete()
    if event.via_bot and is_muted(f"{event.via_bot_id}_{event.chat_id}"):
        await event.delete()


@ultroid_cmd(
    pattern="dmute ?(.*)",
)
async def startmute(event):
    xx = await eor(event, "`Muting...`")
    input = event.pattern_match.group(1)
    private = False
    if event.is_private:
        private = True
    if input:
        if input.isdigit():
            try:
                userid = input
            except ValueError as x:
                return await xx.edit(str(x))
        else:
            userid = (await event.client.get_entity(input)).id
    elif event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eod(xx, "`Reply to a user or add their userid.`", time=5)
    chat_id = event.chat_id
    chat = await event.get_chat()
    if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
        if chat.admin_rights.delete_messages is True:
            pass
        else:
            return await eor(xx, "`No proper admin rights...`", time=5)
    elif "creator" in vars(chat) or private:
        pass
    else:
        return await eod(xx, "`No proper admin rights...`", time=5)
    if is_muted(f"{userid}_{chat_id}"):
        return await eod(xx, "`This user is already muted in this chat.`", time=5)
    try:
        mute(f"{userid}_{chat_id}")
        await eod(xx, "`Successfully muted...`", time=3)
    except Exception as e:
        await eod(xx, "Error: " + f"`{str(e)}`")


@ultroid_cmd(
    pattern="undmute ?(.*)", type=["official", "manager"], ignore_dualmode=True
)
async def endmute(event):
    xx = await eor(event, "`Unmuting...`")
    private = False
    input = event.pattern_match.group(1)
    if event.is_private:
        private = True
    if input:
        if input.isdigit():
            try:
                userid = input
            except ValueError as x:
                return await xx.edit(str(x))
        else:
            userid = (await event.client.get_entity(input)).id
    elif event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eod(xx, "`Reply to a user or add their userid.`", time=5)
    chat_id = event.chat_id
    if not is_muted(f"{userid}_{chat_id}"):
        return await eod(xx, "`This user is not muted in this chat.`", time=3)
    try:
        unmute(f"{userid}_{chat_id}")
        await eod(xx, "`Successfully unmuted...`", time=3)
    except Exception as e:
        await eod(xx, "Error: " + f"`{str(e)}`")


@ultroid_cmd(
    pattern="tmute",
    groups_only=True,
    type=["official", "manager"],
    ignore_dualmode=True,
)
async def _(e):
    xx = await eor(e, "`Muting...`")
    huh = e.text.split(" ")
    try:
        tme = huh[1]
    except BaseException:
        return await eod(xx, "`Time till mute?`", time=5)
    try:
        input = huh[2]
    except BaseException:
        pass
    chat = await e.get_chat()
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
        name = (await e.client.get_entity(userid)).first_name
    elif input:
        if input.isdigit():
            try:
                userid = input
                name = (await e.client.get_entity(userid)).first_name
            except ValueError as x:
                return await xx.edit(str(x))
        else:
            userid = (await e.client.get_entity(input)).id
            name = (await event.client.get_entity(userid)).first_name
    else:
        return await eod(xx, "`Reply to someone or use its id...`", time=3)
    if userid == ultroid_bot.uid:
        return await eod(xx, "`I can't mute myself.`", time=3)
    try:
        bun = await ban_time(xx, tme)
        await e.client.edit_permissions(
            chat.id,
            userid,
            until_date=bun,
            send_messages=False,
        )
        await eod(
            xx,
            f"`Successfully Muted` [{name}](tg://user?id={userid}) `in {chat.title} for {tme}`",
            time=5,
        )
    except BaseException as m:
        await eod(xx, f"`{str(m)}`")


@ultroid_cmd(
    pattern="unmute ?(.*)",
    groups_only=True,
    type=["official", "manager"],
    ignore_dualmode=True,
)
async def _(e):
    xx = await eor(e, "`Unmuting...`")
    input = e.pattern_match.group(1)
    chat = await e.get_chat()
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
        name = (await e.client.get_entity(userid)).first_name
    elif input:
        if input.isdigit():
            try:
                userid = input
                name = (await e.client.get_entity(userid)).first_name
            except ValueError as x:
                return await xx.edit(str(x))
        else:
            userid = (await e.client.get_entity(input)).id
            name = (await e.client.get_entity(userid)).first_name
    else:
        return await eod(xx, "`Reply to someone or use its id...`", time=3)
    try:
        await e.client.edit_permissions(
            chat.id,
            userid,
            until_date=None,
            send_messages=True,
        )
        await eod(
            xx,
            f"`Successfully Unmuted` [{name}](tg://user?id={userid}) `in {chat.title}`",
            time=5,
        )
    except BaseException as m:
        await eod(xx, f"`{str(m)}`")


@ultroid_cmd(
    pattern="mute ?(.*)",
    groups_only=True,
    type=["official", "manager"],
    ignore_dualmode=True,
)
async def _(e):
    xx = await eor(e, "`Muting...`")
    input = e.pattern_match.group(1)
    chat = await e.get_chat()
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
        name = (await e.client.get_entity(userid)).first_name
    elif input:
        if input.isdigit():
            try:
                userid = input
                name = (await e.client.get_entity(userid)).first_name
            except ValueError as x:
                return await xx.edit(str(x))
        else:
            userid = (await e.client.get_entity(input)).id
            name = (await e.client.get_entity(userid)).first_name
    else:
        return await eod(xx, "`Reply to someone or use its id...`", time=3)
    if userid == ultroid_bot.uid:
        return await eod(xx, "`I can't mute myself.`", time=3)
    try:
        await e.client.edit_permissions(
            chat.id,
            userid,
            until_date=None,
            send_messages=False,
        )
        await eod(
            xx,
            f"`Successfully Muted` [{name}](tg://user?id={userid}) `in {chat.title}`",
        )
    except BaseException as m:
        await eod(xx, f"`{str(m)}`")
