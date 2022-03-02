import requests
from discord.ext import commands
from bs4 import BeautifulSoup  # HTML을 파싱하는 모듈

site_link = 'https://www.gamemeca.com/ranking.php'


class GOTY(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='게임순위')
    async def server_status(self, ctx):
        response = requests.get(site_link)
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.select('table.ranking-table tbody > tr')
        _description = "[게임 순위]\n"

        for index, element in enumerate(div, 1):
            name = element.select_one('div.game-name a').get_text()
            _description += f'{index}. {name}\n'

        _description += '\n 출처 : https://www.gamemeca.com/ranking.php'

        _embed = discord.Embed(title='페이퍼봇 정보', description=_description, color=0x00ff00)
        await ctx.send(embed=_embed)
