import discord
from discord.ext import commands

TOKEN = 'NDY0MDIxMTcxNzQ3MjkxMTM3.Dh45CQ.uXa_FzlmTX6N2ke9McTtKmavk18'

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot Online')

client.run(TOKEN)

