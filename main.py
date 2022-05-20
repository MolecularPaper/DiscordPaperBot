import discord
import os
from discord.ext import commands

from Commands import info, todays_meal, discord_status, game_ranking, reaction, song, calculation

prefix = '페이퍼 '

bot = commands.Bot(command_prefix=prefix)
c_reaction = reaction.ReAction(bot)

# command
bot.add_cog(info.Info(bot))
bot.add_cog(game_ranking.Ranking(bot))
bot.add_cog(todays_meal.Meal(bot))
bot.add_cog(discord_status.Status(bot))
bot.add_cog(c_reaction)
bot.add_cog(calculation.Calculation(bot))

# Game
# bot.add_cog(mafia_game.Mafia(bot))

# Song
bot.add_cog(song.Song(bot))

# Event
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=None)
    print("봇 이름", bot.user.name, "봇아이디: ", bot.user.id, "봇 버전: ", discord.__version__)
    print("페이퍼봇 준비 완료!")


@bot.event
async def on_message(msg):
    if msg.content.startswith(prefix):
        await bot.process_commands(msg)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await c_reaction.send_msg(prefix, ctx)


if os.path.isfile('./Data/token.txt'):
    f = open('./Data/token.txt')
    bot.run(f.readline())
else:
    bot.run(os.environ['token'])
