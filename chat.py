import discord
from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='페이퍼')
    async def call_paper_kr(self, ctx, *args):
        str = ' '.join(args)
        if str == "ㅎㅇ":
            await ctx.send('ㅎㅇ')
        if str == "병신":
            await ctx.send('ㄹㅇ ㅋㅋ')
