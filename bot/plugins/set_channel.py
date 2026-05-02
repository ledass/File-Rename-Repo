from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import RPCError, ChatWriteForbidden
from ..database import set_channel, del_channel, get_channel
from bot import bot

@bot.on_message(filters.command("delchannel") & filters.private)
async def delchannel(client: Client, m: Message):
    channel = await get_channel(m.from_user.id)
    if not channel:
        return await m.reply("You don’t have any channel set yet. Use `/setchannel id` first.", quote=True)

    await del_channel(m.from_user.id)
    await m.reply("Your channel has been deleted successfully ❌", quote=True)
  
@bot.on_message(filters.command("setchannel") & filters.private)
async def setchannel(client: Client, m: Message):
    if await get_channel(m.from_user.id):
        await m.reply("You already have a channel set. Only one channel is allowed for now.", quote=True)
        return
    if len(m.command) == 1:
        return await m.reply(
            "Please send the channel id too.\nExample: `/setchannel -1001234567890`",
            quote=True
        )

    try:
        chat_id = int(m.command[1])
    except ValueError:
        return await m.reply("That doesn’t look like a valid channel id.", quote=True)

    try:
        chat = await client.get_chat(chat_id)
    except RPCError:
        return await m.reply(f"Couldn't find that chat", quote=True)

    try:
        bot_member = await client.get_chat_member(chat_id, "me")
    except RPCError:
        return await m.reply("I’m not in that channel. Add me first.", quote=True)

    if bot_member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await m.reply("I’m not an admin there. Make me admin first.", quote=True)

    try:
        user_member = await client.get_chat_member(chat_id, m.from_user.id)
    except RPCError:
        return await m.reply("You’re not in that channel.", quote=True)

    if user_member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await m.reply("That’s not your channel. You need to be admin or owner to link it.", quote=True)
    try:
        msg = await client.send_message(chat_id, "✅ Bot linked successfully.")
        await msg.delete()
    except ChatWriteForbidden:
        return await m.reply("I can’t send messages there. Turn on ‘Send Messages’.", quote=True)
    await set_channel(m.from_user.id, chat_id)
    await m.reply(f"Channel `{chat.title}` has been set successfully ✅", quote=True)
