import random
import discord
from discord.ext import commands


class Meal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.menu = open('./Data/menu.txt', 'r', encoding="UTF-8").readlines()

    @commands.command(name='식사추천')
    async def raffle(self, ctx, *args):
        send_menu = ""
        if args:
            if int(args[0]) > 10:
                await ctx.send('10개 이하만 추천 가능합니다.')
                return
            
            for x in range(int(args[0])):
                send_menu += f'{x + 1}. {random.choice(self.menu)}'
        else:
            send_menu += f'1. {random.choice(self.menu)}\n'

        _embed = discord.Embed(title='추천메뉴', description=send_menu, color=0x00ff00)
        await ctx.send(embed=_embed)
