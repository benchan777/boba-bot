from boba_bot.models import User, Base
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from yelpapi import YelpAPI
import discord
from discord.ext import commands
import os

load_dotenv()
yelp_api = YelpAPI(os.getenv('yelp_api_key'), timeout_s = 3.0)

bot = commands.Bot(command_prefix = '$', intents = discord.Intents.all()) #Initialize discord bot
engine = create_engine('sqlite:///database.db') #Create SQLAlchemy engine
Base.metadata.create_all(engine) #Create database tables
Session = sessionmaker(engine) #Define Session class
Session.configure(bind = engine) #Connect Session class to the engine
db = Session() #Initialize Session class as db

#Removes the first (trigger) word from user bot call
def remove_first_word(string):
    string_list = string.split(' ')
    omit_first_word = string_list[1:]
    new_string = ' '.join(omit_first_word)
    return new_string

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(pass_context = True)
async def test(ctx):
    print(ctx.message.author)
    print(ctx.author.id)
    new_user = User(
        user_id = ctx.message.author.id,
        username = f"{ctx.message.author.name}#{ctx.message.author.discriminator}"
    )
    db.add(new_user)
    db.commit()

@bot.command(pass_context = True)
async def location(ctx, *args):
    location = ' '.join(args)
    user = db.query(User).filter_by(user_id = ctx.message.author.id).one()
    user.location = location
    db.commit()

    for new_location in db.query(User.location).filter_by(user_id = ctx.message.author.id):
        await ctx.send(f"{new_location[0]} has been set as {ctx.message.author.mention}'s location!")

@bot.command(pass_context = True)
async def boba(ctx, *args):
    for i in db.query(User.location).filter_by(user_id = ctx.message.author.id):
        location = i

    if location[0] is None:
        location = ' '.join(args)
        result = yelp_api.search_query(term = 'boba', location = location, categories = 'Bubble Tea')
        store_info = result['businesses']

        store_names = []
        for store in store_info:
            store_names.append(store['name'])

        print('using user specified location')
        await ctx.send(f"Displaying stores in {location}: {store_names}")
    
    else:
        # stored_location = db.query(User.location).filter_by(user_id = message.author.id)
        result = yelp_api.search_query(term = 'boba', location = location, categories = 'Bubble Tea')
        store_info = result['businesses']

        store_names = []
        for store in store_info:
            store_names.append(store['name'])
        
        print('using stored location')
        await ctx.send(f"Your stored location is {location[0]}!\nDisplaying boba stores in {location[0]}:\n{store_names}")

# #Functions to be triggered depending on user input
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return