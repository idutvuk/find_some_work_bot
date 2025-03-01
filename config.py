import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split(',')))
TELETHON_POLLING_INTERVAL = int(os.getenv("TELETHON_POLLING_INTERVAL", 60))
