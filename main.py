import discord
import os
from discord.ext import commands
from Game import mafia_game
from Commands import info, todays_meal, discord_status, game_ranking
from Song import song

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=None)
    print("봇 이름", bot.user.name, "봇아이디: ", bot.user.id, "봇 버전: ", discord.__version__)
    print("페이퍼봇 준비 완료!")


# command
bot.add_cog(info.Info(bot))
bot.add_cog(game_ranking.Ranking(bot))
bot.add_cog(todays_meal.Meal(bot))
bot.add_cog(discord_status.Status(bot))

# Game
bot.add_cog(mafia_game.Mafia(bot))

# Song
bot.add_cog(song.Song(bot))

if os.path.isfile('token.txt'):
    f = open('token.txt')
    bot.run(f.readline())
else:
    bot.run(os.environ['token'])
