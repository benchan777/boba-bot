from boba_bot.main import client
from dotenv import load_dotenv
import os

load_dotenv()

client.run(os.getenv('discord_bot_token'))