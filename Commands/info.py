import discord
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        bot.remove_command("help")
        self.bot = bot

    async def execution(self, ctx):
        _description = '이 봇은 MolecularPaper가 제작하였습니다.\n\n 제작을 도와준사람(닉네임): 누군가'
        _embed = discord.Embed(title='페이퍼봇 정보', description=_description, color=0x00ff00)
        await ctx.send(embed=_embed)

    @commands.command(name='Info')
    async def paper_info_en(self, ctx):
        await self.execution(ctx)

    @commands.command(name='정보')
    async def paper_info_kr(self, ctx):
        await self.execution(ctx)