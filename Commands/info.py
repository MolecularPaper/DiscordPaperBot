import discord
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 봇 정보
    @commands.command(name='정보')
    async def info_bot(self, ctx):
        _description = '이 봇은 MolecularPaper가 제작하였습니다.'
        _embed = discord.Embed(title='페이퍼봇 정보', description=_description, color=0x00ff00)
        await ctx.send(embed=_embed)

    # 명령어 정보
    @commands.command(name='명령어')
    async def info_command(self, ctx):
        _embed = discord.Embed(title='명령어 정보', description='페이퍼 명령어 - 페이퍼봇의 명령어를 알려줍니다.'
                                                           '\n\n 페이퍼 정보 - 페이퍼봇의 기본적인 정보를 알려줍니다.'
                                                           '\n\n 페이퍼 서버상태 - 디스코드 서버의 상태를 알려줍니다. '
                                                           '\n\n 페이퍼 식사추천 - 식사를 추천해줍니다 '
                                                           '\n\n 페이퍼 게임순위 - 현재 게임 순위를 알려줍니다.', color=0x00ff00)
        await ctx.send(embed=_embed)
