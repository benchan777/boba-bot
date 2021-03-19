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

@bot.event
async def on_ready():
    for guild in bot.guilds:
        for member in guild.members:
            user = db.query(User.username).filter_by(user_id = member.id).first()

            if user is None:
                new_user = User(
                    user_id = member.id,
                    username = f"{member.name}#{member.discriminator}",
                    server_id = guild.id,
                    server_name = guild.name
                )
                db.add(new_user)
                db.commit()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    for guild in bot.guilds:
        for member in guild.members:
            user = db.query(User.username).filter_by(user_id = member.id).first()

            if user is None:
                new_user = User(
                    user_id = member.id,
                    username = f"{member.name}#{member.discriminator}",
                    server_id = guild.id,
                    server_name = guild.name
                )
                db.add(new_user)
                db.commit()
    

@bot.command(pass_context = True)
async def location(ctx, *args):
    location = ' '.join(args)
    user = db.query(User).filter_by(user_id = ctx.message.author.id).one()
    user.location = location
    db.commit()

    new_location = db.query(User.location).filter_by(user_id = ctx.message.author.id).one()
    await ctx.send(f"{new_location} has been set as {ctx.message.author.mention}'s location!")

@bot.command(pass_context = True)
async def boba(ctx, *args):
    location = db.query(User.location).filter_by(user_id = ctx.message.author.id)

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
        result = yelp_api.search_query(term = 'boba', location = location, categories = 'Bubble Tea')
        store_info = result['businesses']

        store_names = []
        for store in store_info:
            store_names.append(store['name'])
        
        print('using stored location')
        await ctx.send(f"Your stored location is {location[0]}!\nDisplaying boba stores in {location[0]}:\n{store_names}")

@bot.command(pass_context = True)
async def store_members(ctx):
    for member in ctx.guild.members:
        user = db.query(User.username).filter_by(user_id = member.id).first()

        if user is None:
            new_user = User(
                user_id = member.id,
                username = f"{member.name}#{member.discriminator}"
            )
            db.add(new_user)
            db.commit()

# #Functions to be triggered depending on user input
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return