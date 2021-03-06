from boba_bot.main import db
from boba_bot.models import User, Base, BobaShop
import discord
from discord.ext import commands

#Function to create discord embeds with store information
def store_info_embed(name, url, description, thumbnail, rating, price, phone, open_now, color):
    embed = discord.Embed(title = name, url = url, description = description, color = color) #Default required information for embeds
    embed.set_thumbnail(url = thumbnail) #Embed thumbnail url

    #Discord embed returns an error if the length of the value field is 0
    embed_1 = 'N/A' if len(str(rating)) == 0 else rating
    embed_2 = 'N/A' if len(str(price)) == 0 else price
    embed_3 = 'N/A' if len(str(phone)) == 0 else phone
    embed_4 = 'N/A' if len(str(open_now)) == 0 else open_now

    #Additional discord embed fields
    embed.add_field(name = 'Rating', value = embed_1, inline = True)
    embed.add_field(name = 'Price', value = embed_2, inline = True)
    embed.add_field(name = 'Phone Number', value = embed_3, inline = True)
    embed.add_field(name = 'Open Now', value = embed_4, inline = True)

    return embed

#Function to save searched store information into database
def save_store_info(name, id, city):
    store_db = db.query(BobaShop).filter_by(store_id = id).first()

    #Only adds stores to database if they do not already exist to prevent duplicates
    if store_db is None:
        new_store = BobaShop(
            name = name,
            store_id = id,
            city = city
        )
        db.add(new_store)
        db.commit()