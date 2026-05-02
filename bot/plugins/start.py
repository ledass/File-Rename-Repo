from bot import bot
from pyrogram import filters
from ..database import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@bot.on_callback_query(filters.regex("^help"))
async def help(_, cq):
    text = (
        "**Here’s a quick guide:**\n\n"
        "/setchannel – Choose the channel where renamed files will be sent. Make sure I’m admin and can post messages there.\n\n"
        "/delchannel – Remove the channel so renamed files go back to your PM.\n\n"
        "/setcaption - Set a custom caption for your files.\n\n"
        "**Example:**\n`/setcaption File: {name}\nSize: {size}`\n\n"
        "/setmetadata - Add metadata for your files.\n\n"
        "**Example:**\n`/setmetadata Uploaded by @FileRenameebot`\n\n"
        "/autorename - Automatically rename files as document or video.\n\n"
        "/delcaption, /delmetadata, /delthumb - Remove saved settings.\n\n"
        "Send a photo to set it as your file thumbnail."
    )
    btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🏠 Home", callback_data="home")]]
    )
    await cq.message.edit_text(text, reply_markup=btn, disable_web_page_preview=True)

@bot.on_callback_query(filters.regex("^home"))
async def home(_, cq):
    buttons = [
        [
            InlineKeyboardButton("⚙️ Help", callback_data="help"),
        ],
        [
            InlineKeyboardButton("🌐 Support Chat", url="https://t.me/XBOTSUPPORTS"),
            InlineKeyboardButton("📢 Update Channel", url="https://t.me/BeesonsBots")
        ]
    ]

    await cq.message.edit_text(
        f"""👋 Hey {cq.from_user.mention},

I'm a Rename Bot
I can rename your files ultra fast ⚡  
and even let you change thumbnails easily!

Just send me a file to get started.
""",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    
@bot.on_message(filters.command("start") & filters.private)
async def start(_, m):
    await save_user(m)
    buttons = [
        [
            InlineKeyboardButton("⚙️ Help", callback_data="help"),
            InlineKeyboardButton("GitHub", url="https://github.com/Beesonn/RenameBot"),
        ],
        [
            InlineKeyboardButton("🌐 Support Chat", url="https://t.me/XBOTSUPPORTS"),
            InlineKeyboardButton("📢 Update Channel", url="https://t.me/BeesonsBots")
        ]
    ]

    await m.reply_text(
        f"""👋 Hey {m.from_user.mention},

I'm a Rename Bot
I can rename your files ultra fast ⚡  
and even let you change thumbnails easily!

Just send me a file to get started.
""",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
  
