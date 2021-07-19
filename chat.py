import discord
from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def paper_help_en(self, ctx): await self.paper_help_kr(self, ctx)

    @commands.command(name='도움말')
    async def paper_help_kr(self, ctx):
        _embed = discord.Embed(title='페이퍼 도움말 제목', description='페이퍼 도움말 설명', color=0x00ff00)
        _embed.add_field(name='도움말1', value='여기에 도움말 1 이 추가됩니다! - line1', inline=True)
        _embed.add_field(name='도움말2', value='여기에 도움말 2 이 추가됩니다! - line2', inline=True)
        _embed.add_field(name='도움말3', value='여기에 도움말 3 이 추가됩니다! - line3', inline=True)
        _embed.add_field(name='도움말4', value='여기에 도움말 4 이 추가됩니다! - line4', inline=True)
        _embed.add_field(name='도움말5', value='여기에 도움말 5 이 추가됩니다! - line5', inline=True)
        _embed.set_footer(text='페이퍼 하단 설명')
        await ctx.send(embed=_embed)

    @commands.command(name='페이퍼')
    async def call_paper_kr(self, ctx, *args):
        str = ' '.join(args)
        if str == "ㅎㅇ":
            await ctx.send('ㅎㅇ')
        if str == "병신":
            await ctx.send('ㄹㅇ ㅋㅋ')
