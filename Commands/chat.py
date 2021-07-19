import json

import discord
from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('reaction_data.json', "r") as json_file:
            self.reaction_dic = json.load(json_file)

    async def show_command_info(self, ctx):
        _embed = discord.Embed(title='명령어 정보', description='!페이퍼 <문장> 을 입력하면 저와 대화할 수 있습니다. 심심하면 불러주세요.'
                                                           '\n !페이퍼 알려주기 <문장> : <대답> 을 입력하면 제가 모르는 문장을 알려줄 수 있습니다!',
                               color=0x00ff00)
        await ctx.send(embed=_embed)

    async def add_reaction(self, ctx, *args):
        str_list = list(args[0])
        del str_list[0]
        temp = ' '.join(str_list)

        # 제대로 입력됬는지 확인
        if temp.count(':') > 1:
            ctx.send('잘못 입력하였습니다!')
            return None

        # 알려준 문장 등록
        recation = temp.split(':')
        self.reaction_dic[recation[0].strip()] = (recation[1].strip(), ctx.message.author.name)
        with open('reaction_data.json', "w") as json_file:
            json.dump(self.reaction_dic, json_file, ensure_ascii=False, indent='\t')
        await ctx.send('등록되었습니다!')

    @commands.command(name='페이퍼')
    async def call_paper_kr(self, ctx, *args):
        try:
            str = args[0]
            if str == '정보' or str == 'Info':
                await self.show_command_info(ctx)
            elif str == '알려주기':
                await self.add_reaction(ctx, args)
            elif str in self.reaction_dic:
                await ctx.send(self.reaction_dic[str][0])
            else:
                await ctx.send('ㅇ?')
        except:
            await self.show_command_info(ctx)
