import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        bot.remove_command("help")
        self.bot = bot

    async def execution(self, ctx):
        _description = '간략한 도움말입니다. 자세한 정보는 밑에를 참고해주세요!'\
                       '\n\n!Info or 정보 : 페이퍼 봇의 정보를 표시합니다.\n' \
                       '\n!command or 명령어 : 명령어 관련 도움말을 표시합니다.\n' \
                       '\n!페이퍼 <문장>: 페이퍼와 대화할 수 있습니다.\n'

        _embed = discord.Embed(title='페이퍼 도움말', description=_description, color=0x00ff00)
        await ctx.send(embed=_embed)

    @commands.command(name='help')
    async def paper_help_en(self, ctx):
        await self.execution(ctx)

    @commands.command(name='도움말')
    async def paper_help_kr(self, ctx):
        await self.execution(ctx)
