import secret
import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import json, os
import random
from helpers import getHoroscope, getJoke, getMovies


TOKEN = secret.creds['token']

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
        await asyncio.sleep(300)

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

@client.command()
async def coinflip():
    turnout = ''
    toss = random.randint(0,1)
    if toss == 0:
        turnout = 'heads'
    else:
        turnout = 'tails'

    await client.say(turnout)

@client.command()
async def horoscope(*args):
    sunsign, date, horoscope, mood, keywords, intensity = getHoroscope(args[0])
    horoscope_embed = discord.Embed(
        title = 'Daily Zodiac Horoscope - ' + sunsign,
        color = discord.Color.blue()
    )
    horoscope_embed.add_field(name='Todays Reading', value=horoscope, inline=False)
    horoscope_embed.add_field(name='Mood', value=mood, inline=False)
    horoscope_embed.add_field(name='Keywords', value=keywords, inline=False)
    horoscope_embed.add_field(name='Intensity', value=intensity, inline=False)
    await client.say(embed=horoscope_embed)

@client.command()
async def movies():
    now_showing_movies, coming_soon_movies = getMovies()
    
    now_showing = '\r\n'.join(now_showing_movies)
    coming_soon = '\r\n'.join(coming_soon_movies)

    movie_embed = discord.Embed(
        title = 'Movies in QFX Cinemas',
        color = discord.Color.green()
    )
    movie_embed.add_field(name='Now Showing', value=now_showing, inline=False)
    movie_embed.add_field(name='Coming Soon', value=coming_soon, inline=False)
    await client.say(embed=movie_embed)

@client.command()
async def joke():
    joke = getJoke()
    await client.say(joke)

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
