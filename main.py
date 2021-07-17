import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=None)
    print("봇 이름", bot.user.name, "봇아이디: ", bot.user.id, "봇 버전: ", discord.__version__)


@bot.event()
async def on_message(message):
    if message.author.bot:
        return None

    if message.content.startwith('!안녕'):
        channel = message.channel
        await  channel.send('ㅎㅇ')


@bot.command()
async def hello(ctx):
    await ctx.send('ㅎㅇ')


bot.run(os.environ['token'])
