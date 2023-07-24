import os
from pathlib import Path

from dotenv import load_dotenv

# Set BASE_DIR for all project
BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

# Load env
load_dotenv(BASE_DIR / '../.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Current language
LANG = 'en'  # en, uk
