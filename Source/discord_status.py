import requests
from discord.ext import commands
from bs4 import BeautifulSoup  # HTML을 파싱하는 모듈

site_link = 'https://discordstatus.com/'

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='서버상태')
    async def server_status(self, ctx):
        response = requests.get(site_link)
        soup = BeautifulSoup(response.content, 'html.parser')
        status = soup.select_one('span[class="status font-large"]').get_text()
        await ctx.send(status)
