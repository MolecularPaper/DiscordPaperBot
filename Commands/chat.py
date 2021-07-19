import json, asyncio, discord
from Commands import reaction
from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction = reaction.Reaction()
        # reaction_data.json의 파일의 인코딩이 UTF-8이여야 한다. 안그럼 오류남
        with open('reaction_data.json', "r") as json_file:
            self.reaction_dic = json.load(json_file)

    async def show_command_info(self, ctx):
        _embed = discord.Embed(title='명령어 정보', description='!페이퍼 <문장> 을 입력하면 저와 대화할 수 있습니다. 심심하면 불러주세요.'
                                                           '\n !페이퍼 알려주기 <문장> : <대답> 을 입력하면 제가 모르는 문장을 알려줄 수 있습니다.'
                                                           '\n !페이퍼 기억삭제 <문장> 을 입력하면 제가 기억속에서 해당 문장을 지울 수 있습니다. '
                                                           '(입력자가 알려줬을경우만 삭제됨)',
                               color=0x00ff00)
        await ctx.send(embed=_embed)

    @commands.command(name='페이퍼')
    async def call_paper_kr(self, ctx, *args):
        try:
            str = args[0]
            if str == '정보' or str == 'Info':
                await self.show_command_info(ctx)
            elif str == '알려주기':
                await self.add_reaction(ctx, args)
            elif str == '기억삭제':
                await self.reaction.delete_reaction(ctx, args)
            else:
                await self.reaction.reaction(ctx, str)
        except:
            await self.show_command_info(ctx)
