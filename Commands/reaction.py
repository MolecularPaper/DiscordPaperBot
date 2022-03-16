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
        elif msg == '병신':
            await self.send_edit(ctx, '**지는ㅋ**', '뭐', 0.5)
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