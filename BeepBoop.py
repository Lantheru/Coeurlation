import os
import random
import discord
import MarketApp
from dotenv import load_dotenv
import dataframe_image as dfi

servers = ['Balmung', 'Brynhildr', 'Coeurl', 'Diabolos', 'Goblin', 'Malboro', 'Mateus', 'Zalera']

bot = MarketApp.CoeurlConnection(user="bbbot")

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
    message.content = message.content.lower()

    if 'help' in message.content:
        await message.channel.send('My current commands are: help, test')
        break

    if 'bb!' in message.content:
        _logmessage(message)

        
        if 'test' in message.content:
            # for type in ['salehistory', 'currentlistings']:
            #     if type in message.content:
            #         query = Uniquery(querytype = type)
            
            
            
            _makefile(worldlist)

            await message.channel.send(file = discord.File('df_img.png'))

client.run(TOKEN)