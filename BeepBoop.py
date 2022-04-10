import os
import random
import discord
import MarketApp
from MarketApp import *
import pandas
from dotenv import load_dotenv
import dataframe_image as dfi
import re

servers = ['Balmung', 'Brynhildr', 'Coeurl', 'Diabolos', 'Goblin', 'Malboro', 'Mateus', 'Zalera']

def _makefile(df):
    dfi.export(df, 'df_img.png')

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


@client.event
async def on_ready():
    for guild in client.guilds:
        print(guild)
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'help' in message.content:
        await message.channel.send('My current commands are: help, test')
        return

    if 'bb!' in message.content:
        _logmessage(message)

        
        if 'test' in message.content:
            if 'itemlookup' in message.content:
                user_string = re.search(r'"(.*?)"',message.content)
                user_string = user_string.group()
                print(user_string)
                data = bot.itemlookup(user_string)
                if len(data) == 0:
                    await message.channel.send('I did not find the thing, sheeeiiiit.')
                    

                if len(data) > 50:
                    await message.channel.send('bruh be more specific. That produced {} results'.format(len(data)))
                    
                if len(data) <= 50 and len(data) > 0:
                    _makefile(data)
                    await message.channel.send(file = discord.File('df_img.png'))
            # for type in ['salehistory', 'currentlistings']:
            #     if type in message.content:
            #         query = Uniquery(querytype = type)
            
            
            
            # _makefile(worldlist)

            

client.run(TOKEN)