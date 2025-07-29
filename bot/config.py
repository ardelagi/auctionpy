import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'auction_bot')
ADMIN_ROLE_ID = int(os.getenv('ADMIN_ROLE_ID', 0))
DEFAULT_TIMER = int(os.getenv('DEFAULT_TIMER', 300))  # 5 menit default