import discord
from discord.ext import commands
from Source import utility

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_info = utility.read_file('command_info')
        self.paper_info = utility.read_file('paper_info')

    # 봇 정보
    @commands.command(name='정보')
    async def info_bot(self, ctx):
        _embed = discord.Embed(title='페이퍼봇 정보', description=self.paper_info, color=0x00ff00)
        await ctx.send(embed=_embed)

    # 명령어 정보
    @commands.command(name='명령어')
    async def info_command(self, ctx):
        _embed = discord.Embed(title='명령어 정보', description=self.command_info, color=0x00ff00)
        await ctx.send(embed=_embed)
