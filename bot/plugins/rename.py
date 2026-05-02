from bot import bot
from pyrogram import filters
from pyrogram.types import *
from ..alt import *
import time
from ..database import *
import os
from pyrogram.enums import MessageMediaType
import asyncio
import os
import re

def clean_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)    
    unwanted = [
        "join", "channel", "t.me", "telegram", "all", "new", "here", "uploaded", "download", "exclusive", "watch"
    ]
    cleaned = re.sub(r"@\w+", "", name)
    cleaned = re.sub(r"https?://\S+", "", cleaned)

    for word in unwanted:
        cleaned = re.sub(rf"\b{word}\b", "", cleaned, flags=re.IGNORECASE)

    cleaned = re.sub(r"[_\-]+", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned.title() + ext


async def add_metadata(input_path, output_path, metadata):
    try:
        command = [
            'ffmpeg', '-y', '-i', input_path, '-map', '0', '-c:s', 'copy', '-c:a', 'copy', '-c:v', 'copy',
            '-metadata', f'title={metadata}',
            '-metadata', f'author={metadata}',  
            '-metadata:s:s', f'title={metadata}',  
            '-metadata:s:a', f'title={metadata}',  
            '-metadata:s:v', f'title={metadata}',  
            '-metadata', f'artist={metadata}',  
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        print(e_response)
        print(t_response)

        
        if os.path.exists(output_path):
            return output_path
        else:
            return None
    except Exception as e:
        print(f"Error Occurred While Adding Metadata : {str(e)}")
        return None

@bot.on_message(filters.private & (filters.document | filters.video))
async def rnm_p(bot, message):
    file = getattr(message, message.media.value)
    if file.file_size > 2000 * 1024 * 1024:
        await message.reply(
            "😅 Sorry, I can’t handle files larger than 2GB for renaming.\n\n"
            "💡 A small donation would help me upgrade and support bigger files!",
            quote=True
        )
        return

    if await get_autorename(message.from_user.id):
        mode = await get_autorename_mode(message.from_user.id)
        if mode == "Video":
            await rename_video(bot, message)
            return 
        elif mode == "Document":
            await rename_document(bot, message)
            return 
    await message.reply(
        f"**Please send me the new file name...**\n\n**Current File Name:** `{file.file_name}`",
        quote=True,
        reply_markup=ForceReply(True)
    )


@bot.on_message(filters.private & filters.reply)
async def rename_file(client, message):
    reply_message = message.reply_to_message
    if reply_message.reply_markup and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = file.document or file.video
        
        if not media:
            return None

        if "." not in new_name:
            if "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = f"{new_name}.{extn}"
        await reply_message.delete()
        buttons = [[InlineKeyboardButton("📄 Document", callback_data="document")]]
       # if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
        buttons.append([InlineKeyboardButton("🎥 Video", callback_data="video")])

        await message.reply(
            text=f"**Select one of the options below 👇**\n\n**File Name:** `{new_name}`",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@bot.on_callback_query(filters.regex("^video"))
async def upload_video(bot, update):
    if not os.path.exists(f"metadata/{update.from_user.id}"):
        os.makedirs(f"metadata/{update.from_user.id}")
    new_name = update.message.text
    new_filename = new_name.split(":")[1]
    file_path = f"downloads/{update.from_user.id}/{new_filename.strip()}"
    mfile_path = f"metadata/{update.from_user.id}/{new_filename.strip()}"
    m = await update.message.edit("**Downloading...**")
    file = update.message.reply_to_message
  #  media = getattr(file, file.media.value)

    try:
        path = await bot.download_media(
            message=file,
            file_name=file_path,
            progress=progress_message,
            progress_args=("Downloading...", m, time.time())
        )
    except Exception as e:
        print(e)
        await m.edit("**Something went wrong!**\n\nPlease contact our support chat: @XBOTSUPPORTS")
        return

    metadata = await get_metadata(update.from_user.id)
    if metadata:
        metapath = await add_metadata(file_path, mfile_path, metadata)       
    await m.edit("**Uploading...**")
    thumb = await get_thumb(update.from_user.id)
    tf = await bot.download_media(thumb) if thumb else None

    caption = await get_caption(update.from_user.id)
    pname, _ = os.path.splitext(new_filename)
    caption = caption.format(name=pname, size=humanbytes(media.file_size)) if caption else f"**{pname}**"
    ch_id = await get_channel(update.from_user.id)
    try:
        await bot.send_video(
            chat_id=ch_id if ch_id else update.message.chat.id,
            video=metapath if metadata else file_path,
            caption=caption,
            thumb=tf,
            progress=progress_message,
            progress_args=("Uploading...", m, time.time())
        )
    except:
        if ch_id:
            await m.edit("Couldn't send the file to the channel. Make sure I'm an admin and have permission to post messages.")
            return 
        else:
            await m.edit("**Something went wrong!**\n\nPlease contact our support chat: @XBOTSUPPORTS")
            return
    if os.path.exists(file_path):
        os.remove(file_path)
    if tf and os.path.exists(tf):       
        os.remove(tf)
    if metadata and os.path.exists(mfile_path):
        os.remove(metapath)
    await m.delete()


@bot.on_callback_query(filters.regex("^document"))
async def upload_document(bot, update):
    if not os.path.exists(f"metadata/{update.from_user.id}"):
        os.makedirs(f"metadata/{update.from_user.id}")
    new_name = update.message.text
    new_filename = new_name.split(":")[1]
    file_path = f"downloads/{update.from_user.id}/{new_filename.strip()}"
    mfile_path = f"metadata/{update.from_user.id}/{new_filename.strip()}"
    m = await update.message.edit("**Downloading...**")
    file = update.message.reply_to_message
    media = getattr(file, file.media.value)

    try:
        path = await bot.download_media(
            message=file,
            file_name=file_path,
            progress=progress_message,
            progress_args=("Downloading...", m, time.time())
        )
    except Exception as e:
        print(e)
        await m.edit("**Something went wrong!**\n\nPlease contact our support chat: @XBOTSUPPORTS")
        return

    metadata = await get_metadata(update.from_user.id)
    if metadata:
        metapath = await add_metadata(file_path, mfile_path, metadata)       
    await m.edit("**Uploading...**")
    thumb = await get_thumb(update.from_user.id)
    tf = await bot.download_media(thumb) if thumb else None

    caption = await get_caption(update.from_user.id)
    pname, _ = os.path.splitext(new_filename)
    caption = caption.format(name=pname, size=humanbytes(media.file_size)) if caption else f"**{pname}**"
    ch_id = await get_channel(update.from_user.id)
    try:
        await bot.send_document(
            chat_id=ch_id if ch_id else update.message.chat.id,
            document=metapath if metadata else file_path,
            caption=caption,
            thumb=tf,
            progress=progress_message,
            progress_args=("Uploading...", m, time.time())
        )
    except:
        if ch_id:
            await m.edit("Couldn't send the file to the channel. Make sure I'm an admin and have permission to post messages.")
            return 
        else:
            await m.edit("**Something went wrong!**\n\nPlease contact our support chat: @XBOTSUPPORTS")
            return
    if os.path.exists(file_path):
        os.remove(file_path)
    if tf and os.path.exists(tf):       
        os.remove(tf)
    if metadata and os.path.exists(mfile_path):
        os.remove(metapath)
    await m.delete()

@bot.on_callback_query(filters.regex("^cancel"))
async def cancel(bot, query):
    try:
        await query.message.delete()
        await query.message.reply_to_message.delete()
        await query.message.continue_propagation()
    except:
        await query.message.delete()
        await query.message.continue_propagation()

async def rename_video(bot, message):
    if not os.path.exists(f"metadata/{message.from_user.id}"):
        os.makedirs(f"metadata/{message.from_user.id}")
    media = getattr(message, message.media.value)
    metadata = await get_metadata(message.from_user.id)
    new_filename = metadata + " " + clean_filename(media.file_name) if metadata else clean_filename(media.file_name)
    file_path = f"downloads/{message.from_user.id}/{new_filename}"
    mfile_path = f"metadata/{message.from_user.id}/{new_filename}"
    m = await message.reply("**Downloading...**")

    try:
        path = await bot.download_media(
            message=message,
            file_name=file_path,
            progress=progress_message,
            progress_args=("Downloading...", m, time.time())
        )
    except Exception as e:
        print(e)
        await m.edit("**Something went wrong!**\n\nPlease contact our support chat: @XBOTSUPPORTS")
        return

    if metadata:
        metapath = await add_metadata(file_path, mfile_path, metadata)       
    await m.edit("**Uploading...**")
    thumb = await get_thumb(message.from_user.id)
    tf = await bot.download_media(thumb) if thumb else None

    caption = await get_caption(message.from_user.id)
    pname, _ = os.path.splitext(new_filename)
    caption = caption.format(name=pname, size=humanbytes(media.file_size)) if caption else f"**{pname}**"
    ch_id = await get_channel(message.from_user.id)
    try:
        await bot.send_video(
            chat_id=ch_id if ch_id else message.chat.id,
            video=metapath if metadata else file_path,
            caption=caption,
            thumb=tf,
            progress=progress_message,
            progress_args=("Uploading...", m, time.time())
        )
    except:
        if ch_id:
            await m.edit("Couldn't send the file to the channel. Make sure I'm an admin and have permission to post messages.")
            return 
        else:
            await m.edit("**Something went wrong!**\n\nPlease contact our support chat: @XBOTSUPPORTS")
            return
    if os.path.exists(file_path):
        os.remove(file_path)
    if tf and os.path.exists(tf):       
        os.remove(tf)
    if metadata and os.path.exists(mfile_path):
        os.remove(metapath)
    await m.delete()

async def rename_document(bot, message):
    if not os.path.exists(f"metadata/{message.from_user.id}"):
        os.makedirs(f"metadata/{message.from_user.id}")
    media = getattr(message, message.media.value)
    metadata = await get_metadata(message.from_user.id)
    new_filename = metadata + " " + clean_filename(media.file_name) if metadata else clean_filename(media.file_name)
    file_path = f"downloads/{message.from_user.id}/{new_filename}"
    mfile_path = f"metadata/{message.from_user.id}/{new_filename}"
    m = await message.reply("**Downloading...**")

    try:
        path = await bot.download_media(
            message=message,
            file_name=file_path,
            progress=progress_message,
            progress_args=("Downloading...", m, time.time())
        )
    except Exception as e:
        print(e)
        await m.edit("**Something went wrong!**\n\nPlease contact our support chat: @XBOTSUPPORTS")
        return

    if metadata:
        metapath = await add_metadata(file_path, mfile_path, metadata)       
    await m.edit("**Uploading...**")
    thumb = await get_thumb(message.from_user.id)
    tf = await bot.download_media(thumb) if thumb else None

    caption = await get_caption(message.from_user.id)
    pname, _ = os.path.splitext(new_filename)
    caption = caption.format(name=pname, size=humanbytes(media.file_size)) if caption else f"**{pname}**"
    ch_id = await get_channel(message.from_user.id)
    try:
        await bot.send_document(
            chat_id=ch_id if ch_id else message.chat.id,
            document=metapath if metadata else file_path,
            caption=caption,
            thumb=tf,
            progress=progress_message,
            progress_args=("Uploading...", m, time.time())
        )
    except:
        if ch_id:
            await m.edit("Couldn't send the file to the channel. Make sure I'm an admin and have permission to post messages.")
            return 
        else:
            await m.edit("**Something went wrong!**\n\nPlease contact our support chat: @XBOTSUPPORTS")
            return
    if os.path.exists(file_path):
        os.remove(file_path)
    if tf and os.path.exists(tf):       
        os.remove(tf)
    if metadata and os.path.exists(mfile_path):
        os.remove(metapath)
    await m.delete()
    
    
