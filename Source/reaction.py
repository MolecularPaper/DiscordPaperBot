import random, os
from discord.ext import commands
from Source import utility

reaction_file_path = './Data/reaction.txt'

class ReAction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.use_gpt = False
        self.reactions = self.read_reaction()

    # 리액션 읽기
    def read_reaction(self):
        reactions = {}
        
        if not os.path.isfile(reaction_file_path):
            return reactions

        f = open(reaction_file_path, 'r', encoding="UTF-8")
        lines = f.readlines()
        
        for line in lines:
            if not line:
                continue
            split = line.split(' : ')
            if reactions.get(split[0]) is None:
                reactions[split[0]] = [split[1].replace("\n", "")]
            else:
                reactions[split[0]].append(split[1].replace("\n", ""))
        return reactions

    @commands.command(name='배워')
    async def learn(self, ctx, word, *args):
        text = ' '.join(args)
        if ['명령어', '정보', '서버상태', '식사추천', '게임순위'].__contains__(word):
            await ctx.send('어림도 없지!')
            return
        if self.reactions.get(word) != None and self.reactions[word].__contains__(text):
            await ctx.send('이미 배웠습니다!')
            return
        if text.isspace():
            await ctx.send('반응할 문장을 입력해주세요!')
            return
        
        if self.reactions.get(word) is None:
            self.reactions[word] = [text]
        else:
            self.reactions[word].append(text)
            
        await ctx.send(f'{word} - {text}, 확인했습니다.')

        with open(reaction_file_path, 'a', encoding="UTF-8") as f:
            f.write(f"{word} : {text}\n")

    async def send_msg(self, prefix, ctx):
        msg = ctx.message.content.replace(prefix, "")
        if msg == '팬텀워커':
            await utility.send_edit(ctx.channel, '개같은 주인놈...', '**위대하고 뛰어난 저의 창조주십니다!**', 0.3)
        elif msg == '병신':
            await utility.send_edit(ctx.channel, '**지는ㅋ**', '뭐', 0.5)
        elif msg in self.reactions:
            await ctx.channel.send(random.choice(self.reactions[msg]))
        else:
            await ctx.send('ㅇ?')
        return False