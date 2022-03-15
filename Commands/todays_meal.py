import random
from discord.ext import commands


class Meal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='식사추천')
    async def raffle(self, ctx, *args):
        f = open('menu.txt', 'r', encoding="UTF-8")
        menu = f.readlines()

        if args:
            if int(args[0]) > 10:
                await ctx.send('10개 이하만 추천 가능합니다.')
                return
            
            for x in range(int(args[0])):
                await ctx.send(f'추천할 메뉴: {random.choice(menu)}')
        else:
            await ctx.send(f'추천할 메뉴: {random.choice(menu)}')
