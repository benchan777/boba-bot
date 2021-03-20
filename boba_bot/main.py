from boba_bot.models import User, Base, BobaShop
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from yelpapi import YelpAPI
import discord
from discord.ext import commands
import os

load_dotenv()
yelp_api = YelpAPI(os.getenv('yelp_api_key'), timeout_s = 3.0) #Initialize Yelp api

bot = commands.Bot(command_prefix = '$', intents = discord.Intents.all()) #Initialize discord bot
engine = create_engine('sqlite:///database.db') #Create SQLAlchemy engine
Base.metadata.create_all(engine) #Create database tables
Session = sessionmaker(engine) #Define Session class
Session.configure(bind = engine) #Connect Session class to the engine
db = Session() #Initialize Session class as db
from boba_bot.functions import store_info_embed, save_store_info

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

#Adds new members to database on join
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
    
#Sets the user's location in the database
@bot.command(pass_context = True)
async def location(ctx, *args):
    location = ' '.join(args)
    user = db.query(User).filter_by(user_id = ctx.message.author.id).one()
    user.location = location
    db.commit()

    new_location = db.query(User.location).filter_by(user_id = ctx.message.author.id).one()
    await ctx.send(f"{new_location[0]} has been set as {ctx.message.author.mention}'s location!")

#Displays information of boba stores near the specified location
@bot.command(pass_context = True)
async def boba(ctx, *args):
    location = db.query(User.location).filter_by(user_id = ctx.message.author.id).first()
    print(location[0])

    #If the user has no saved location, use the input location
    if location[0] is None:
        #Queries Yelp api for boba stores near input location
        location = ' '.join(args)
        result = yelp_api.search_query(term = 'boba', location = location, categories = 'Bubble Tea')
        store_info = result['businesses']

        #Iterate through all found stores
        for store in store_info:
            #Some stores do not have price info and a key error will be returned. This mitigates that
            try:
                price = store['price']
            except:
                price = 'N/A'

            #Calls function to display store information in embed format in channel chat
            embed = store_info_embed(
                store['name'],
                store['url'],
                f"{store['location']['address1']} {store['location']['city']}, {store['location']['state']} {store['location']['zip_code']}",
                store['image_url'],
                store['rating'],
                price,
                store['phone']
                )
            await ctx.send(embed = embed)

            save_store_info(store['name'], store['id'], store['location']['city'])

        print('using user specified location')
    
    #If the user has a saved location, use the saved location
    else:
        #Queries Yelp api for boba stores near input location
        result = yelp_api.search_query(term = 'boba', location = location, categories = 'Bubble Tea')
        store_info = result['businesses']

        #Iterate through all found stores
        for store in store_info:
            #Some stores do not have price info and a key error will be returned. This mitigates that
            try:
                price = store['price']
            except:
                price = 'N/A'

            #Calls function to display store information in embed format in channel chat
            embed = store_info_embed(
                store['name'],
                store['url'],
                f"{store['location']['address1']} {store['location']['city']}, {store['location']['state']} {store['location']['zip_code']}",
                store['image_url'],
                store['rating'],
                store['price'],
                store['phone']
                )
            await ctx.send(embed = embed)

            save_store_info(store['name'], store['id'], store['location']['city'])
        
        print('using stored location')

#Save the user's desired order to the specified boba shop
@bot.command(pass_context = True)
async def order(ctx, store, *order_info):
    user = db.query(User).filter_by(user_id = ctx.message.author.id).one()

    user.user_order.append(db.query(BobaShop).filter_by(name = store).one())
    user.user_order_info = ' '.join(order_info)
    db.add(user)
    db.commit()

    await ctx.send(f"You have set {db.query(User.user_order_info).filter_by(user_id = ctx.message.author.id).first()[0]} as your desired drink from {store}!")

#Displays user orders that are tied to the input store name
@bot.command(pass_context = True)
async def store(ctx, *name):
    pass