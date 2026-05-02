import os
from pyrogram import Client

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
TOKEN = os.getenv("BOT_TOKEN")

if not API_ID or not str(API_ID).isdigit():
    print("❌ API_ID is missing or invalid")
    exit(1)

if not API_HASH:
    print("❌ API_HASH is missing")
    exit(1)

if not TOKEN or ":" not in TOKEN:
    print("❌ BOT_TOKEN is missing or invalid")
    exit(1)

API_ID = int(API_ID)

bot = Client(
    "renm",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="bot"),
    # max_concurrent_transmissions=7,
    workers=200,
    sleep_threshold=15,
)
