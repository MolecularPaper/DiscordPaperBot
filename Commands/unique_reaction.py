import asyncio, os


async def check_reaction(ctx, str):
    if str == '최진원' and ctx.message.author.name != '최진원':
        await unique_reaction_1(ctx)
        return True
    elif str == '병신' or str == 'ㅄ' or str == 'ㅂㅅ':
        await unique_reaction_1(ctx)
        return True


async def unique_reaction_1(ctx):
    m = await ctx.send('그는 안탑갑게도 탈모...')
    await asyncio.sleep(0.5)
    await m.edit(content='ㅇ?')

async def unique_reaction_2(ctx):
    m = await ctx.send('시발 능력도 없는 새끼 주제에... ')
    await asyncio.sleep(0.5)
    await m.edit(content='ㅇ?')