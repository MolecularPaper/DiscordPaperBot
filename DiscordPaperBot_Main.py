import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)


bot.run('ODIzNTM2NzA2NDU1NzMyMjM0.YFiQUw.6RB8vzpHCGqNiGOvUsq-St5NZHA')
