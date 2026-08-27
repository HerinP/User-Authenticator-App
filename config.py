from dotenv import load_dotenv
import os

load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
SCRIPT_EMAIL = os.getenv("SCRIPT_EMAIL")
SCRIPT_EMAIL_PASS = os.getenv("SRIPT_EMAIL_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER") 
DB_PASS = os.getenv("DB_PASS")