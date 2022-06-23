import random, os
from discord.ext import commands

class RockScissorsPaper(commands.Cog):
    def __init__(self, bot):
         self.bot = bot
    
    @commands.command(name='가위바위보')
    async def learn(self, ctx, p_state):
        b_state = random.randrange(1, 3)
        p_state = 0 if p_state == '가위' else 1 if p_state == '바위' else 2 if p_state =='보' else -1

        if p_state < 0:
            await ctx.send("입력이 잘못되었습니다.")
            return
        
        result = p_state - b_state
        states = ['가위', '바위', '보']
        send = "무승부" if result == 0 else "플레이어 승리!" if result > 0 else "봇 승리!"
        await ctx.send(f"페이퍼: {states[b_state]}, {send}")
