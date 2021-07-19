import json
from Commands import unique_reaction


class Reaction:
    def __init__(self):
        # reaction_data.json의 파일의 인코딩이 UTF-8이여야 한다. 안그럼 오류남
        with open('reaction_data.json', "r") as json_file:
            self.reaction_dic = json.load(json_file)

    async def reaction(self, ctx, str):
        try:
            if not await unique_reaction.check_reaction(ctx, str):
                await ctx.send(self.reaction_dic[str][0])
        except:
            await ctx.send('ㅇ?')

    async def add_reaction(self, ctx, *args):
        str_list = list(args[0])
        del str_list[0]
        temp = ' '.join(str_list)

        # 제대로 입력됬는지 확인
        if temp.count(':') > 1:
            ctx.send('잘못 입력하였습니다!')
            return None

        # 이미 등록되있는지 확인
        recation = temp.split(':')
        if recation[0].strip() in self.reaction_dic:
            await ctx.send('이미 등록되어있습니다!')
            return None

        # 알려준 문장 등록
        self.reaction_dic[recation[0].strip()] = (recation[1].strip(), ctx.message.author.name)
        with open('reaction_data.json', "w") as json_file:
            json.dump(self.reaction_dic, json_file, ensure_ascii=False, indent='\t')
        await ctx.send('등록되었습니다!')

    async def delete_reaction(self, ctx, *args):
        str_list = list(args[0])
        del str_list[0]
        str = ' '.join(str_list)

        # 등록된 문장인지와 등록자가 본인인지 확인후, 맞으면 제거후 확인 메세지 출력, 아니면 메세지 출력후 종료
        if not (str in self.reaction_dic):
            await ctx.send('등록되있지 않은 문장입니다!')
        elif self.reaction_dic[str][1] != ctx.message.author.name:
            await ctx.send('등록한 사람이 다릅니다!')
        else:
            del self.reaction_dic[str]
            await ctx.send('삭제되었습니다!')
            with open('reaction_data.json', "w") as json_file:
                json.dump(self.reaction_dic, json_file, ensure_ascii=False, indent='\t')
