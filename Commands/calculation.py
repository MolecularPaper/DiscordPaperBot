from tabnanny import check
from discord.ext import commands

class Calculation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='계산')
    async def calculation(self, ctx, *args):
        text = ""
        for arg in args:
            text += arg
        
        if  self.bracket_check(text) is False:
            await ctx.send("괄호 개수가 맞지 않습니다.")
            return
        
        await ctx.send(text)

    # 괄호 유효성 체크
    def bracket_check(self, text: str) -> bool:
        check_count = 0

        for char in list(text):
            check_count += 1 if char == "(" else -1 if char == ")" else 0

        return check_count == 0