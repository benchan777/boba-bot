from boba_bot.models import User, Base
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from yelpapi import YelpAPI
import discord
import os

load_dotenv()
yelp_api = YelpAPI(os.getenv('yelp_api_key'), timeout_s = 3.0)

client = discord.Client()
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
Session.configure(bind = engine)
db = Session()

def remove_first_word(string):
    string_list = string.split(' ')
    omit_first_word = string_list[1:]
    new_string = ' '.join(omit_first_word)
    return new_string

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$test'):
        print(message.author.id)
        new_user = User(
            name = 'test_name',
            username = 'test_username'
        )
        db.add(new_user)
        db.commit()

    if message.content.startswith('$boba'):
        location = remove_first_word(message.content)
        result = yelp_api.search_query(term = 'boba', location = location, categories = 'Bubble Tea')
        store_info = result['businesses']

        store_names = []
        for store in store_info:
            store_names.append(store['name'])

        await message.channel.send(store_names)