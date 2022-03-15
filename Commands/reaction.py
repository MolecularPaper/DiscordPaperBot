import discord
import random
import asyncio
from discord.ext import commands

coms = ['질긴종이', '최진원', '이명재', '돌침대', '조병현']
reactions = {}


def read_reaction():
    f = open('./Data/reaction.txt', 'r', encoding="UTF-8")
    lines = f.readlines()

    for line in lines:
        split = line.split(' : ')
        if reactions.get(split[0]) is None:
            reactions[split[0]] = [split[1]]
            coms.append(split[0])
        else:
            reactions[split[0]].append(split[1])


class Reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        read_reaction()

    @commands.command(aliases=coms)
    async def send_msg(self, ctx):
        msg = ctx.message.content.replace("페이퍼 ", "")

        if msg == '질긴종이':
            await self.send_edit(ctx, '개같은 주인놈...', '**위대하고 뛰어난 저의 창조주십니다!**', 0.3)
        elif msg == '최진원':
            await self.send_edit(ctx, '안탑갑게도 그는 대머리...', 'ㅇ?', 0.5)
        elif msg == '이명재':
            await self.send_edit(ctx, '병신 ㅋㅋ', '그게 누구임?', 0.5)
        elif msg == '조병현':
            await self.send_edit(ctx, '머저리에 병신에... 팀 프로젝트를 던지지 않나... 난 살면서 이런 개새끼를 첨봤어...', "뭐 ", 0.3)
        elif msg in reactions:
            await ctx.send(random.choice(reactions[msg]))

    @commands.command(name='배워')
    async def learn(self, ctx, arg1, arg2):
        if reactions.get(arg1) is None:
            reactions[arg1] = [arg2]
            coms.append(arg1)
            print(coms)
        else:
            reactions[arg1].append(arg2)
        await ctx.send(f'{arg1} = {arg2}, 확인했습니다.')



    async def send_edit(self, ctx, send_msg, edit_msg, delay):
        tk = await ctx.send(send_msg)
        await asyncio.sleep(delay)
        await tk.edit(content=edit_msg)