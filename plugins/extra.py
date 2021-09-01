# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ Commands Available -

• `{i}del <reply to message>`
    Delete the replied message.

• `{i}edit <new message>`
    Edit your last message or replied msg.

• `{i}copy <reply to message>`
    Copy replied message / media.

• `{i}reply`
    Reply the last sent msg to replied user.
"""
import asyncio

from telethon.events import NewMessage as NewMsg

from . import *

_new_msgs = {}


@ultroid_bot.on(
    NewMsg(
        outgoing=True,
    ),
)
async def newmsg(event):
    if event.message.message == f"{HNDLR}reply":
        return
    _new_msgs[event.chat_id] = event.message


@ultroid_cmd(
    pattern="del$",
)
async def delete_it(delme):
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
        except Exception as e:
            await eod(delme, f"Couldn't delete the message.\n\n**ERROR:**\n`{str(e)}`")


@ultroid_cmd(
    pattern="copy$",
)
async def copy(e):
    reply = await e.get_reply_message()
    if reply:
        if reply.text and not reply.media:
            await eor(e, reply.text)
        else:
            await reply.reply(reply)
            if e.out:
                await e.delete()
    else:
        await eod(e, "`Reply To any message`")


@ultroid_cmd(
    pattern="edit",
)
async def editer(edit):
    message = edit.text
    chat = await edit.get_input_chat()
    string = str(message[6:])
    reply = await edit.get_reply_message()
    if reply and reply.text:
        try:
            await reply.edit(string)
            await edit.delete()
        except BaseException:
            pass
    else:
        i = 1
        async for message in edit.client.iter_messages(chat, ultroid_bot.uid):
            if i == 2:
                await message.edit(string)
                await edit.delete()
                break
            i = i + 1


@ultroid_cmd(
    pattern="reply$",
)
async def _(e):
    if e.reply_to_msg_id and e.chat_id in _new_msgs:
        msg = _new_msgs[e.chat_id]
        chat = await e.get_input_chat()
        await asyncio.wait(
            [
                e.client.delete_messages(chat, [e.id, msg.id]),
                e.client.send_message(chat, msg, reply_to=e.reply_to_msg_id),
            ]
        )
    else:
        await e.delete()
