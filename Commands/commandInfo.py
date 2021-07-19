import discord
from discord.ext import commands

command_kr = '\n!정보 : 봇의 정보를 보여줍니다.' \
             '\n!필터링 <active>: 채팅 필터링 기능을 키거나 끕니다. (추가예정)'

command_en = '\n!Info : 봇의 정보를 보여줍니다.' \
             '\n!filtering <active>: 채팅 필터링 기능을 키거나 끕니다. (추가예정)'


class CommandInfo(commands.Cog):
    def __init__(self, bot):
        bot.remove_command("help")
        self.bot = bot

    async def execution(self, ctx, *args):
        str = ' '.join(args[0])

        if args.__len__() > 1:
            return None
        elif str == 'kr':
            await self.show_kr_command(ctx)
        elif str == 'en':
            await self.show_en_command(ctx)
        else:
            await self.show_command_info(ctx)

    async def show_kr_command(self, ctx):

        _embed = discord.Embed(title='페이퍼 명령어', description=f'페이퍼의 한글 명령어 목록입니다.\n\n{command_kr}', color=0x00ff00)
        await ctx.send(embed=_embed)

    async def show_en_command(self, ctx):
        _embed = discord.Embed(title='페이퍼 명령어', description=f'페이퍼의 영문 명령어 목록입니다.\n{command_en}', color=0x00ff00)
        await ctx.send(embed=_embed)

    async def show_command_info(self, ctx):
        _embed = discord.Embed(title='명령어 정보', description='!command or 명령어 <언어> : 입력한 언어의 명령어 목록을 표시합니다. '
                                                           '\n\n(사용가능한 언어 목록: kr, en)', color=0x00ff00)
        await ctx.send(embed=_embed)

    @commands.command(name='command')
    async def paper_info_en(self, ctx, *args):
        await self.execution(ctx, args)

    @commands.command(name='명령어')
    async def paper_info_kr(self, ctx, *args):
        await self.execution(ctx, args)
