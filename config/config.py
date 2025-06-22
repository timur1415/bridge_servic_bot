import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
URL = os.getenv('URL')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
PORT = os.getenv('PORT')
BITRIKS_URL = os.getenv('BITRIKS_URL')