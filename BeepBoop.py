import os
import io
import random
import discord
import MarketApp
from MarketApp import *
import pandas
from dotenv import load_dotenv
import dataframe_image as dfi
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

client = discord.Client()
theDB = CoeurlConnection()

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
        
        
        if 'help' in words:
            await message.channel.send(
                'Hello! Please make sure all commands are preceeded by "bb!". My commands are currently:\n\nLookupitem: Takes a word enveloped by double quotation marks and forms a list of matching names and their FFXIV id numbers.\n**Example**\nbb! lookupitem "materia"\n\nCurrentlisting or Salehistory: Returns instances of the item currently listed in the marketplace or its history of sales in the last week. Please provide server names within @ symbols and separated by commas and item ids within $ symbols separated by commas.\n **Example**\nbb! currentlistings @Coeurl,Balmung@ #6548,7490#'
                                        )
            return

        if 'lookupitem' in words:
            user_string = re.search(r'"(.*?)"',message.content)
            user_string = user_string.group().strip('"')
            data = theDB.itemlookup(user_string)
            if len(data) == 0:
                await message.channel.send('I did not find the thing, sadface dot execute')
                

            if len(data) > 200:
                await message.channel.send('That produced {} results. I\'m limited to 50'.format(len(data)))
                
            if len(data) <= 200 and len(data) > 0:
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
            with io.BytesIO() as temp:
                dfi.export(user_query,temp, max_rows = -1)
                temp.seek(0)
               
                await message.channel.send(file = temp)


client.run(TOKEN)