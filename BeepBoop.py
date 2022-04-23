import os
import io
import random
import discord
import MarketApp
from MarketApp import *
import pandas
from dotenv import load_dotenv
import dataframe_image as dfi
from parameters import paras
import re

servers = ['Balmung', 'Brynhildr', 'Coeurl', 'Diabolos', 'Goblin', 'Malboro', 'Mateus', 'Zalera']


#need to update: records message that prompted a command and saves it into bbtestlog.txt
def _logmessage(message, whattowrite = None):
    message = message
    if whattowrite == None:
        whattowrite = 'input received from {}: "{}" \n'.format(message.author, message.content)

    with open('bbtestlog.txt', 'a') as log:
        log.write(whattowrite)




load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

user = "bbbot"
client = discord.Client()
theDB = psycopg2.connect(database='coeurlation', user=user, password=paras['users'][user])

@client.event
##ready message when logged in
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

## when you read a message, do:
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    words = message.content.lower().split()

    if 'bb!' in words:
        _logmessage(message)
        print(f'request received from {message.author}: {message.content}')
        
        if 'help' in words:
            print("I'm helping...")
            await message.channel.send("""
                                        Hello! Please make sure all commands are preceeded by "bb!". My commands are currently:\n\n
                                        Lookupitem: Takes a word enveloped by double quotation marks and forms a list of matching names and their FFXIV id numbers.\n
                                        **__Example__**\nbb! lookupitem "materia"
                                        \n\ncurrentlisting or salehistory: Returns instances of the item currently listed in the marketplace or its history of sales in the last week. please provide a single server name within @ symbols as well as a single item id within $ symbols. File size limitations make it very hard to transfer
                                        \n **__Example__**\n
                                        bb! currentlistings @Coeurl@ #6548#'
                                        """)
            return

        if 'lookupitem' in words:
            
            user_string = re.search(r'"(.*?)"',message.content)
            user_string = user_string.group().strip('"')
            data = theDB.itemlookup(user_string)
            print(f"Looking up string fragment {user_string}")
            if len(data) == 0:
                print("No Results")
                await message.channel.send('I did not find the thing, sadface dot execute')
                

            if len(data) > 200:
                print("Too many results found")
                await message.channel.send('That produced {} results. I\'m limited to 200'.format(len(data)))
                
            if len(data) <= 200 and len(data) > 0:
                print("Sending dataframe to discord")
                with io.BytesIO() as temp:
                    dfi.export(data,temp, max_rows = -1)
                    temp.seek(0)
                    await message.channel.send(file = discord.File(temp,'lookup.png',))
        
        elif 'currentlistings' or 'salehistory' in words:
            if 'salehistory' in words:
                user_querytype = 'salehistory'
            else:
                user_querytype = 'currentlistings'
            user_world = re.search(r'@(.*?)@',message.content)
            user_world = user_world.group().replace("@","")
           
            user_itemids = re.search(r'\$(.*?)\$',message.content)
           
            user_itemids = user_itemids.group().replace("$","")
            user_query = UniQuery(user_world, user_itemids, user_querytype)
            print(f"{user_querytype} was {len(user_query.df.values)} rows long")

            if len(user_query.df.index) > 5000:
                await message.channel.send('Dataframe exceeded 5,000 entries, just no.')
            else:
                if user_querytype == 'currentlistings':
                    df = user_query.df.drop(['creatorID', 'listingID','retainerCity', 'lastUploadTime', 'lastReviewTime', 'sellerID','isCrafted'], axis=1)
                    df = df.sort_values(['itemID','worldID','pricePerUnit'])
                
                elif user_querytype == 'salehistory':
                    df = user_query.df[['worldID', 'worldName', 'itemName', 'hq', 'pricePerUnit', 'quantity', 'soldAt']]
                    df = df.sort_values(['itemName','worldID','pricePerUnit'])


                await message.channel.send(f"Getting the juice ready....Dataframe is {len(user_query.df.index)} rows long")
                with io.BytesIO() as temp:
                    dfi.export(df,temp, max_rows = -1)
                    temp.seek(0)
                
                
                    await message.channel.send(file = discord.File(temp, 'userquery.png'))


client.run(TOKEN)