import secret
import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import json, os
import random
from helpers import getHoroscope, getJoke, getMovies, getNews


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
        title = 'daily Coffee - List of Commands',
        color = discord.Color.green()
    )
    help_embed.add_field(name='.echo', value='Returns whatever you type', inline = False)
    help_embed.add_field(name='.news', value='Displays top 10 headline news from Nepal', inline = False)
    help_embed.add_field(name='.coinflip', value='Flips a coin and displays either Heads or Tails', inline = False)
    help_embed.add_field(name='.horoscope zodiac', value='Displays daily horoscope of your zodiac', inline = False)
    help_embed.add_field(name='.movies', value='Displays list of movies now showing and coming soon', inline = False)
    help_embed.add_field(name='.joke', value='Displays a yomama joke', inline = False)
    help_embed.add_field(name='.movies', value='Displays list of movies now showing and coming soon', inline = False)
    await client.send_message(author, embed=help_embed)

@client.command()
async def news():
    news_list = getNews()
    news = " - "+ '\r\n- '.join(news_list) 
    news_embed = discord.Embed(
        title = 'Daily News',
        color = discord.Color.green()
    )
    news_embed.add_field(name='Top 10 Headlines from Nepal', value=news, inline=False)
    await client.say(embed=news_embed)

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
    
    now_showing = " - "+ '\r\n- '.join(now_showing_movies)
    coming_soon = " - "+ '\r\n- '.join(coming_soon_movies)

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

client.loop.create_task(change_status())
client.run(TOKEN)   
