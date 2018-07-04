import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import json, os

TOKEN = 'NDY0MDIxMTcxNzQ3MjkxMTM3.Dh45CQ.uXa_FzlmTX6N2ke9McTtKmavk18'

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

# -------------------------------> Event Actions

@client.event
async def on_ready():
    print('Bot Online')

status = ['Paladins', 'Dota 2', 'Fornite', 'PUBG']

async def change_status():
    await client.wait_until_ready()
    status_message = cycle(status)
    while not client.is_closed:
        current_status = next(status_message)
        await client.change_presence(game = discord.Game(name = current_status))
        await asyncio.sleep(3600)

# -------------------------------> Commands

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    help_embed = discord.Embed(
        color = discord.Color.orange()
    )

    help_embed.set_author(name='Help Menu')
    help_embed.add_field(name='.echo', value='Returns whatever you type', inline = True)

    await client.send_message(author, embed=help_embed)

@client.command(pass_context = True)
async def clear(ctx, amount = 100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(str(amount) + ' message(s) deleted.')

@client.command()
async def logout():
    await client.logout()

@client.command()
async def displayembed():
    myembed = discord.Embed(
        title = 'The Title',
        description = 'Some description here...',
        color = discord.Color.blue()
    )
    myembed.set_footer(text = 'This is footer')
    myembed.set_image(url='')
    myembed.set_thumbnail(url='')
    myembed.set_author(name='Author Name', icon_url='')
    myembed.add_field(name='Field Name 1', value='Field Value', inline = True)
    myembed.add_field(name='Field Name 2', value='Field Value', inline = True)
    await client.say(embed=myembed)

client.loop.create_task(change_status())
client.run(TOKEN)   
