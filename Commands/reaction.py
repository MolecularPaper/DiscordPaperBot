import discord
import random
import asyncio
from discord.ext import commands

reactions = {}


def read_reaction():
    f = open('./Data/reaction.txt', 'r', encoding="UTF-8")
    lines = f.readlines()

    for line in lines:
        if not line:
            continue
        split = line.split(' : ')
        if reactions.get(split[0]) is None:
            reactions[split[0]] = [split[1]]
        else:
            reactions[split[0]].append(split[1])


async def send_msg(ctx):
    msg = ctx.content.replace("페이퍼 ", "")
    if msg == '질긴종이':
        await send_edit(ctx.channel, '개같은 주인놈...', '**위대하고 뛰어난 저의 창조주십니다!**', 0.3)
    elif msg == '병신':
        await send_edit(ctx.channel, '**지는ㅋ**', '뭐', 0.5)
    elif msg in reactions:
        await ctx.channel.send(random.choice(reactions[msg]))
    elif msg in ['명령어', '정보', '서버상태', '식사추천', '게임순위']:
        await ctx.channel.send('그건 내 명령어다 애송이')
    else:
        return True
    return False


async def learn(ctx):
    msg = ctx.content.replace("페이퍼 ", "")
    arg1 =
    arg2 =
    if reactions.get(arg1) is None:
        reactions[arg1] = [arg2]
    elif arg2 in reactions[arg1]:
        await ctx.channel.send('이미 배웠습니다!')
        return
    else:
        reactions[arg1].append(arg2)
    await ctx.send(f'{arg1} - {arg2}, 확인했습니다.')
    f = open('./Data/reaction.txt', 'a', encoding="UTF-8")
    f.write(f"{arg1} : {arg2}\n")


async def send_edit(channel, msg, edit_msg, delay):
    tk = await channel.send(msg)
    await asyncio.sleep(delay)
    await tk.edit(content=edit_msg)
