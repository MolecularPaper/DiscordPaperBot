import discord
from discord.ext import commands


class Mafia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 봇 정보
    @commands.command(name='마피아게임')
    async def server_status(self, ctx):
