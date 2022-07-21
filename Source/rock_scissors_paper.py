import random, os
from discord.ext import commands

class RockScissorsPaper(commands.Cog):
    def __init__(self, bot):
         self.bot = bot
    
    @commands.command(name='가위바위보')
    async def learn(self, ctx, p_state):
        b_state = random.randrange(0, 2)
        p_state = 0 if p_state == '가위' else 1 if p_state == '바위' else 2 if p_state =='보' else -1

        if p_state < 0:
            await ctx.send("입력이 잘못되었습니다.")
            return
        
        states = ['가위', '바위', '보']
        result = [
            ['무승부', '플레이어 승리!', '봇 승리!'], #가위
            ['봇 승리!', '무승부', '플레이어 승리!'], #바위
            ['플레이어 승리!', '봇 승리!', '무승부'] #보
        ]
        await ctx.send(f"페이퍼: {states[b_state]}, {result[b_state][p_state]}")
