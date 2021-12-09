import discord, os
from Commands import info, chat, commandInfo
from discord.ext import commands
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=None)
    print("봇 이름", bot.user.name, "봇아이디: ", bot.user.id, "봇 버전: ", discord.__version__)
    print("페이퍼봇 준비 완료!")

bot.add_cog(commandInfo.CommandInfo(bot))
bot.add_cog(info.Info(bot))
bot.add_cog(chat.Chat(bot))
bot.run(os.environ['token'])