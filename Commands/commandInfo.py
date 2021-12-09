import discord
from discord.ext import commands

command_kr = '페이퍼 봇의 한글 명령어 목록입니다' \
             '\n\n!정보 : 봇의 정보를 보여줍니다.' \
             '\n\n!페이퍼 : 페이퍼 봇과 대화를 할 수 있습니다.'
             #'\n\n!필터링 <active>: 채팅 필터링 기능을 키거나 끕니다. (추가예정)'

command_en = 'List of command on PaperBot' \
             '\n\n!Info : Show bot info' \
             #'\n\n!filtering <active>: Turn chat filtering on or off. '


async def show_command_info(ctx, lan):
    global _embed
    if lan == 'kr':
        _embed = discord.Embed(title='페이퍼 명령어', description=command_kr, color=0x00ff00)
    elif lan == 'en':
        _embed = discord.Embed(title='페이퍼 명령어', description=command_en, color=0x00ff00)
    await ctx.send(embed=_embed)


class CommandInfo(commands.Cog):
    def __init__(self, bot):
        bot.remove_command("help")
        self.bot = bot

    @commands.command(name='command')
    async def command_en(self, ctx, *args):
        await show_command_info(ctx, 'en')

    @commands.command(name='명령어')
    async def command_kr(self, ctx, *args):
        await show_command_info(ctx, 'kr')

    @commands.command(name='help')
    async def help_en(self, ctx, *args, 'kr'):
        await show_command_info(ctx, 'en')

    @commands.command(name='도움말')
    async def help_kr(self, ctx, *args, 'kr'):
        await show_command_info(ctx, 'kr')
