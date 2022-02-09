import discord
from discord.ext import commands


async def execution(ctx):
    _description = '이 봇은 MolecularPaper가 제작하였습니다.\n\n 제작을 도와준사람(닉네임): 누군가'
    _embed = discord.Embed(title='페이퍼봇 정보', description=_description, color=0x00ff00)
    await ctx.send(embed=_embed)


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

<<<<<<< HEAD
    # 봇 정보
    @commands.command(name='정보')
    async def info_bot(self, ctx):
        _description = '이 봇은 MolecularPaper가 제작하였습니다.'
        _embed = discord.Embed(title='페이퍼봇 정보', description=_description, color=0x00ff00)
        await ctx.send(embed=_embed)

    # 명령어 정보
    @commands.command(name='명령어')
    async def info_command(self, ctx):
        _embed = discord.Embed(title='명령어 정보', description='!정보 - 페이퍼봇의 기본적인 정보를 알려줍니다.'
                                                           '\n\n !서버상태 - 디스코드 서버의 상태를 알려줍니다. ', color=0x00ff00)
        await ctx.send(embed=_embed)
=======
    @commands.command(name='info')
    async def paper_info_en(self, ctx):
        await execution(ctx)

    @commands.command(name='정보')
    async def paper_info_kr(self, ctx):
        await execution(ctx)
>>>>>>> 0087976463b3c8a9c91411afd88a65dd195dad5c
