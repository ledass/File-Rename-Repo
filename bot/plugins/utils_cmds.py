from bot import bot
from pyrogram import filters
from ..database import *
from pyrogram.types import *

@bot.on_message(filters.command("setcaption") & filters.private)
async def setcaption(_, message):
    if len(message.command) == 1:
        await message.reply(
            "**Example:**\n\n"
            "`/setcaption File: {name}\n"
            "Size: {size}`"
        )
        return

    caption = message.text.split(None, 1)[1]
    status = await save_caption(message.from_user.id, caption)

    if status == "saved":
        await message.reply(f"**Caption saved:**\n\n`{caption}`")
    else:
        await message.reply("❌ Failed to save caption, try again later.")

@bot.on_message(filters.command("setmetadata") & filters.private)
async def setmetadata(client, message):
    if len(message.command) == 1:
        await message.reply(
            "**Example:**\n\n"
            "`/setmetadata join @BeesonsBots`"
        )
        return
        
    text = message.text.split(None, 1)[1]
    status = await set_metadata(message.from_user.id, text)

    if status == "saved":
        await message.reply(f"**New metadata:**\n\n`{text}`")
    else:
        await message.reply("❌ Failed to save metadata, try again later.")
        
@bot.on_message(filters.command("delthumb") & filters.private)
async def del_thumbnail(_, m):
    try:
        result = await del_thumb(m.from_user.id)
        if not result:
            await m.reply("**Hmm, looks like you don’t have a thumbnail set 🙄**", quote=True)
        else:
            await m.reply("**Your thumbnail has been successfully deleted.**", quote=True)
    except Exception as e:
        print(e)
        await m.reply("Oops! Something went wrong. Please try again later.", quote=True)

@bot.on_message(filters.command("autorename") & filters.private)
async def autorename_cmd(_, m):
    user_id = m.from_user.id
    data = await get_autorename(user_id)
    mode = await get_autorename_mode(user_id)

    if not data:
        btn = InlineKeyboardMarkup(
            [[InlineKeyboardButton("✅ Enable Auto Rename", callback_data=f"enable_auto_{user_id}")]]
        )
        await m.reply_text(
            "Wanna turn on Auto Rename? once it’s on I’ll rename your files automatically\n\n"
            "You can choose whether your files uploaded as Document or Video",
            reply_markup=btn
        )
    else:
        btn = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔁 Change Mode", callback_data=f"change_mode_{user_id}"),
                InlineKeyboardButton("❌ Turn Off", callback_data=f"disable_auto_{user_id}")
            ]
        ])
        await m.reply_text(
            f"Auto Rename is currently on.\n\n"
            f"**Mode:** `{mode}`\n\n"
            "You can switch modes or disable it below.",
            reply_markup=btn
        )


@bot.on_callback_query(filters.regex(r"^enable_auto"))
async def enable_autorename_cb(_, cq):
    btn = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📄 Document", callback_data="auto_mode_doc"),
            InlineKeyboardButton("🎥 Video", callback_data="auto_mode_vid")
        ]
    ])
    await cq.message.edit_text(
        "Please select your preferred **Auto Rename Mode**:",
        reply_markup=btn
    )


@bot.on_callback_query(filters.regex(r"^change_mode"))
async def change_mode_cb(_, cq):
    btn = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📄 Document", callback_data="auto_mode_doc"),
            InlineKeyboardButton("🎥 Video", callback_data="auto_mode_vid")
        ]
    ])
    await cq.message.edit_text(
        "🔁 **Change Auto Rename Mode**\n\n"
        "Choose your new mode below:",
        reply_markup=btn
    )


@bot.on_callback_query(filters.regex(r"^auto_mode_(doc|vid)"))
async def set_mode_cb(_, cq):
    mode = cq.matches[0].group(1)  # ✅ fixed (no comma!)
    mode_text = "Document" if mode == "doc" else "Video"

    await set_autorename(cq.from_user.id, True, mode_text)
    await cq.message.edit_text(
        f"✅ **Auto Rename enabled successfully**\n\n"
        f"Current Mode: {'📄 Document' if mode_text == 'Document' else '🎥 Video'}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("❌ Turn Off", callback_data=f"disable_auto_{cq.from_user.id}")]]
        )
    )

@bot.on_callback_query(filters.regex(r"^disable_auto"))
async def disable_autorename_cb(_, cq):
    await set_autorename(cq.from_user.id, False, None)
    await cq.message.edit_text(
        "**Auto Rename has been turned off**"
    )
                       
@bot.on_message(filters.command("delmetadata") & filters.private)
async def delmetadata(_, m):
    try:
        result = await del_metadata(m.from_user.id)
        if not result:
            await m.reply("**Hmm, looks like you don’t have a metadata set 🙄**", quote=True)
        else:
            await m.reply("**Your metadata has been successfully deleted.**", quote=True)
    except Exception as e:
        print(e)
        await m.reply("Oops! Something went wrong. Please try again later.", quote=True)
        
@bot.on_message(filters.command("delcaption") & filters.private)
async def delcaption(_, m):    
    result = await del_caption(m.from_user.id)       
    if not result:
        await m.reply("**Hmm, looks like you don’t have a captain set 🙄**", quote=True)      
    else:
        await m.reply("**Your caption has been successfully deleted.**", quote=True)
    
@bot.on_message(filters.photo & filters.private)
async def thumbnail(_, m):
    try:
        result = await save_thumb(m)
        if result == "Error":
            await m.reply("Oops! Couldn't save your thumbnail.", quote=True)
        else:
            await m.reply("**Your thumbnail has been saved.**", quote=True)        
    except Exception as e:
        print(e)
        await m.reply("Something went wrong. Please try again.", quote=True)

