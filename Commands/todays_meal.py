import random
from discord.ext import commands


class Meal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='식사추천')
    async def raffle(self, ctx):
        f = open('menu.txt')
        menu = f.readlines()
        await ctx.send(f'추천할 메뉴: {random.choice(menu)}')
