import asyncio, os


async def check_reaction(ctx, str):
    if str == os.environ['unique_name1'] and ctx.message.author.name != os.environ['unique_name1']:
        await unique_reaction_1(ctx)
        return True


async def unique_reaction_1(ctx):
    m = await ctx.send('그는 안탑갑게도 탈모...')
    await asyncio.sleep(0.5)
    await m.edit(content='ㅇ?')
