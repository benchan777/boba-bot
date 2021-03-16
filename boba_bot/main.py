from boba_bot.models import User, Base
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from yelpapi import YelpAPI
import discord
import os

load_dotenv()
yelp_api = YelpAPI(os.getenv('yelp_api_key'), timeout_s = 3.0)

client = discord.Client()#Initialize discord client so bot can be logged in
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

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

#Functions to be triggered depending on user input
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$test'):
        # print(message.author)
        # print(message.author.id)
        # new_user = User(
        #     user_id = message.author.id,
        #     username = f"{message.author.name}#{message.author.discriminator}"
        # )
        # db.add(new_user)
        # db.commit()
        pass

    #Displays a list of boba shops near user's entered location
    if message.content.startswith('$boba'):
        print(message.author)
        print(message.author.id)
        new_user = User(
            user_id = message.author.id,
            username = f"{message.author.name}#{message.author.discriminator}"
        )
        db.add(new_user)
        db.commit()

        for i in (db.query(User.location).filter_by(user_id = message.author.id)):
            location = i

        if location[0] is None:
            location = remove_first_word(message.content)
            result = yelp_api.search_query(term = 'boba', location = location, categories = 'Bubble Tea')
            store_info = result['businesses']

            store_names = []
            for store in store_info:
                store_names.append(store['name'])

            print('using user specified location')
            await message.channel.send(f"Displaying stores in {location}: {store_names}")
        
        else:
            # stored_location = db.query(User.location).filter_by(user_id = message.author.id)
            stored_result = yelp_api.search_query(term = 'boba', location = location, categories = 'Bubble Tea')
            stored_store_info = stored_result['businesses']

            stored_store_names = []
            for store in stored_store_info:
                stored_store_names.append(store['name'])
            
            print('using stored location')
            await message.channel.send(f"Your stored location is {location[0]}! Displaying boba stores in {location[0]}:\n{stored_store_names}")
            
    #Allow user to save their current location
    if message.content.startswith('$location'):
        location = remove_first_word(message.content)
        user = db.query(User).filter_by(user_id = message.author.id).one()
        user.location = location
        db.commit()

        for new_location in db.query(User.location).filter_by(user_id = message.author.id):
            await message.channel.send(f"{new_location[0]} has been set as {message.author.mention}'s location!")