import discord
from discord.ext import commands

import os

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=None)
    print("봇 이름", bot.user.name, "봇아이디: ", bot.user.id, "봇 버전: ", discord.__version__)
    print("페이퍼봇 준비 완료!")


@bot.event
async def on_message(message):
    if message.content == "안녕!":
        await message.channel.send("안녕!")

    await bot.process_commands(message)


@bot.command(name='안녕')
async def hello(ctx):
    await ctx.send('ㅎㅇ')


@bot.command(name='join')
async def voice_join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("음성채널에 들어가있어야 됩니다!")


@bot.command(name='leave')
async def voice_leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("저 음성채널에 안들어가있는데요?")


@bot.command(name='페이퍼')
async def call_paper(ctx, *args):
    str = ' '.join(args)
    if str == "ㅎㅇ":
        await ctx.send('ㅎㅇ')
    if str == "병신":
        await ctx.send('ㄹㅇ ㅋㅋ')


# bot.run(os.environ['token'])
bot.run('ODIzNTM2NzA2NDU1NzMyMjM0.YFiQUw.swXWiHSw8zik-ISz2Y5JbzKf5Yo')
