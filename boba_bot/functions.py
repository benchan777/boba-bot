from boba_bot.main import db
from boba_bot.models import User, Base, BobaShop
import discord
from discord.ext import commands

#Function to create discord embeds with store information
def store_info_embed(name, url, thumbnail):
    embed = discord.Embed(title = name, url = url, description = name, color = 0x7b00ff)
    embed.set_thumbnail(url = thumbnail)
    return embed

#Function to save searched store information into database
def save_store_info(name, id, city):
    store_db = db.query(BobaShop).filter_by(store_id = id).first()

    if store_db is None:
        new_store = BobaShop(
            name = name,
            store_id = id,
            city = city
        )
        db.add(new_store)
        db.commit()