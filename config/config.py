import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
URL = os.getenv("URL")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
PORT = os.getenv("PORT")
BITRIKS_URL = os.getenv("BITRIKS_URL")
BITRIKS_ACCESS_KEY = os.getenv("BITRIKS_ACCESS_KEY")
BITRIKS_LEAD_FILES_FIELD = os.getenv("BITRIKS_LEAD_FILES_FIELD", "UF_CRM_1756635444")
