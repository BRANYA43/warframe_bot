import gettext
import os
from pathlib import Path

from dotenv import load_dotenv

# Set BASE_DIR for all project
BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

# Load env
load_dotenv(BASE_DIR / '../.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Lang
CURRENT_LANG = 'uk'
LANGS = ('en', 'uk')
