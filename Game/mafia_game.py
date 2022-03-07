import asyncio
import discord
import random

from discord.ext import commands

prefix = '마피아'


class Mafia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 변수
        self.revive_member = None
        self.kill_member = None
        self.kill_vote_list = {}
        self.can_search = True

        # 처형 찬반투표
        self.can_execution_vote = False
        self.execution_vote_agree = 0
        self.execution_vote_opposition = 0

        # 맴버
        self.members = {}

        # 채널 관련
        self.channel_list = {}

    # 게임 명령어
    @commands.command(name=prefix)
    async def read_command(self, ctx, *args):
        if args[0] == '시작':
            await self.start_game(ctx)
        elif args[0] == '종료':
            await self.end_game(ctx)
        elif args[0] == '처형':
            await self.execution_vote(ctx, args[1])
        elif args[0] == '처형찬성':
            await self.execution_agree_vote(ctx, True)
        elif args[0] == '처형반대':
            await self.execution_agree_vote(ctx, False)
        elif args[0] == '사살':
            await self.kill_vote(ctx, args[1])
        elif args[0] == '치료':
            await self.revive_user(ctx, args[1])
        elif args[0] == '조사':
            await self.user_research(ctx, args[1])

    # 게임 시작
    async def start_game(self, ctx):
        if bool(self.channel_list):
            await ctx.send('이미 게임이 진행중입니다.')
            return

        print(f'[마피아게임] ========== 게임 시작 ==========')

        self.channel_list['category'] = await self.create_channel(ctx, '마피아게임', discord.ChannelType.category)
        self.channel_list['lobby'] = await self.create_channel(ctx, '대기', discord.ChannelType.voice,
                                                               category=self.channel_list['category'])
        self.channel_list['g_voice'] = await self.create_channel(ctx, '음성', discord.ChannelType.voice,
                                                                 category=self.channel_list['category'], can_read=False,
                                                                 can_send=False)
        self.channel_list['g_chat'] = await self.create_channel(ctx, '공용', discord.ChannelType.text,
                                                                category=self.channel_list['category'], can_read=False,
                                                                can_send=False)
        self.channel_list['m_chat'] = await self.create_channel(ctx, '마피아', discord.ChannelType.text,
                                                                category=self.channel_list['category'], can_read=False,
                                                                can_send=False)
        self.channel_list['d_chat'] = await self.create_channel(ctx, '의사', discord.ChannelType.text,
                                                                category=self.channel_list['category'], can_read=False,
                                                                can_send=False)
        self.channel_list['p_chat'] = await self.create_channel(ctx, '경찰', discord.ChannelType.text,
                                                                category=self.channel_list['category'], can_read=False,
                                                                can_send=False)
        await self.waiting_join(ctx)

    # 게임참가 대기
    async def waiting_join(self, ctx):
        _embed = discord.Embed(title='마피아게임', description='게임에 참여할려면 마피아게임-대기 채널에 참가해주세요.'
                                                          '\n게임을 하기 위해서는 최소 4명 이상의 인원이 필요합니다.'
                                                          '\n게임은 20초 후에 시작되며, 이후 진행 상황은 마피아게임-공용-채팅에 나타납니다.'
                               , color=0x00ff00)
        await ctx.send(embed=_embed)
        await asyncio.sleep(20)

        _members = self.channel_list['lobby'].members
        if len(_members) >= 4:
            await self.channel_list['g_chat'].send('게임을 시작합니다.')
            for member in _members:
                await self.connect_user_voice(member, self.channel_list['g_voice'])
                await self.set_channel_permissions(member, self.channel_list['lobby'], False)
                await self.set_channel_permissions(member, self.channel_list['g_chat'])
                self.channel_list[f'{member.name}_vote'] = await self.create_channel(ctx, f'{member.name}-투표',
                                                                                     discord.ChannelType.text,
                                                                                     category=self.channel_list[
                                                                                         'category'], can_read=False,
                                                                                     can_send=False)
            await self.assign_role()
            await self.loop(ctx)
        else:
            await ctx.send('인원이 부족하므로 게임을 중단합니다.')
            await asyncio.sleep(2)
            await self.end_game(ctx)

    # 역할 뽑기
    async def assign_role(self):
        await self.channel_list['g_chat'].send('역할을 지정합니다. 개인 메세지를 확인해주세요.')

        # 역할 지정
        members = self.channel_list['g_voice'].members
        members = random.sample(members, len(members))
        for i, member in enumerate(members):
            await self.set_role(member, i)

        await asyncio.sleep(8)

    # 역할 설정
    async def set_role(self, member, role_num):
        mafia_count = 1 if len(self.members) <= 7 else (2 if len(self.members) <= 11 else 3)
        if role_num == 0:
            role = '의사'
            await self.set_channel_permissions(member, self.channel_list['d_chat'], can_send=False)
        elif role_num == 1:
            role = '경찰'
            await self.set_channel_permissions(member, self.channel_list['p_chat'], can_send=False)
        elif 2 <= role_num <= 1 + mafia_count:
            role = '마피아'
            await self.set_channel_permissions(member, self.channel_list['m_chat'], can_send=False)
        else:
            role = '시민'

        self.members[member.name] = (member, role)
        await self.send_dm(member, f'당신의 역할은 {role} 입니다.')
        print(f'[마피아게임] {member.name}의 역할이 {role}로 설정됨')

    # 낮/밤 루프
    async def loop(self, ctx):
        while True:
            await self.night()
            await asyncio.sleep(2)
            if await self.day():
                break
        await asyncio.sleep(5)
        await self.channel_list['g_chat'].send('게임을 종료합니다.')
        await self.end_game(ctx)

    # 밤 진행
    async def night(self):
        print(f'[마피아게임] ========== 밤 ==========')

        # 메세지 전송후 채널내 모든유저 뮤트
        await self.channel_list['g_chat'].send('밤이 되었습니다...')
        await self.all_voice_mute(True)
        await self.all_chat_mute(self.channel_list['g_chat'], False)

        # 직업 채널 활성화
        await asyncio.sleep(0.5)
        self.can_search = True
        await self.set_active_role_channel(True)

        # 직업 채널별 투표
        await self.start_vote_role_channel()

        # 25초간 대기
        await asyncio.sleep(25)

        # 직업채널 비활성화
        await self.set_active_role_channel(False)

        # 사살 목표 확정
        await self.kill_user()
        return

    # 낮 진행
    async def day(self):
        print(f'[마피아게임] ========== 낮 ==========')

        # 메세지 전송후 채널내 모든유저 뮤트 해제
        await self.channel_list['g_chat'].send('낮이 되었습니다.')
        await self.all_voice_mute(False)
        await self.all_chat_mute(self.channel_list['g_chat'], True)
        await self.change_ghost()

        # 밤에 일어난일 설명
        await asyncio.sleep(0.5)
        if self.kill_member is None:
            await self.channel_list['g_chat'].send('아무일도 일어나지 않았습니다...')
        else:
            await self.channel_list['g_chat'].send(f'<{self.kill_member.name}> 가 사망하였습니다.')
            if await self.check_game():
                return True
        await self.kill_vote_reset()
        await asyncio.sleep(0.5)

        # 토론
        chat_time = 15 * len(self.channel_list['g_voice'].members)
        await self.channel_list['g_chat'].send(f'토론을 시작합니다.\n토론은 {chat_time}초간 진행됩니다.')
        await asyncio.sleep(chat_time)

        # 처형투표
        await self.channel_list['g_chat'].send(f'처형 투표를 시작합니다.\n 25초간 진행되며, <자신닉네임>-투표 채널에서 처형투표할 수 있습니다.')
        await self.set_active_execution_vote(True, send_message=f'!{prefix} 처형 <유저이름> 으로 처형투표를 할 수 있습니다.', send_user_list=True)
        await asyncio.sleep(25)

        # 투표 종료
        await self.set_active_execution_vote(False)
        await self.kill_user(is_execution=True)

        # 투표 확인
        if self.kill_member is not None:
            # 최후의 반론
            await self.all_chat_mute(self.channel_list['g_chat'], False)
            await self.set_channel_permissions(self.kill_member, self.channel_list['g_chat'], can_send=True)
            await self.channel_list[f'g_chat'].send(f'최후의 반론을 진행합니다.')
            await asyncio.sleep(15)

            # 찬반투표
            self.can_execution_vote = True
            await self.set_channel_permissions(self.kill_member, self.channel_list['g_chat'], can_send=False)
            await self.set_active_execution_vote(True, send_message=f'찬반투표를 진행합니다.\n!{prefix} 사형찬성/사형반대 로 투표할 수 있습니다.')
            await asyncio.sleep(10)

            if self.execution_vote_agree > self.execution_vote_opposition:
                await self.change_ghost()
            else:
                await self.kill_vote_reset()

        return False

    # 게임 진행상황 확인
    async def check_game(self):
        print(f'[마피아게임] ========== 게임 진행상황 확인 ==========')

        mafia_count = 0
        citizen_count = 0
        for member in self.members.values():
            if member[1] == '마피아':
                mafia_count += 1
            else:
                citizen_count += 1

        if mafia_count == 0:
            await self.channel_list['g_chat'].send('시민 승리!')
            return True
        elif mafia_count >= citizen_count:
            await self.channel_list['g_chat'].send('마피아 승리!')
            return True

        return False

    # 처형 투표
    async def execution_agree_vote(self, ctx, value: bool):
        if ctx.channel is self.channel_list[f'{ctx.author.name}_vote']:
            if value:
                self.execution_vote_agree += 1
            else:
                self.execution_vote_opposition += 1
            await self.set_channel_permissions(ctx.author, self.channel_list[f'{ctx.author.name}_vote'], can_send=True)
            print(f'[마피아게임] {ctx.name}가 {("찬성" if value else "반대")}함')

    # 처형 투표
    async def execution_vote(self, ctx, name: str):
        if ctx.channel == self.channel_list[f'{ctx.author.name}_vote']:
            await self.kill_vote(ctx, name, send_vote_list=False)
            print(f'[마피아게임] {self.kill_member.name}가 {name}을 처형투표함')
        return

    # 사살 투표 리셋
    async def kill_vote_reset(self):
        self.kill_member = None
        self.kill_vote_list = {}

    # 사살 투표
    async def kill_vote(self, ctx, name, send_vote_list: bool = True):
        if self.members.get(name) is None:
            await self.channel_list['m_chat'].send('없는 유저 입니다.')
        elif ctx.channel is self.channel_list['m_chat']:
            self.kill_vote_list[ctx.author.name] = self.members[name][0]
            if send_vote_list:
                await self.send_kill_vote_list()
            print(f'[마피아게임] {ctx.author.name} 가 {name}을 사살투표함')

    # 사살 목표 확정
    async def kill_user(self, is_execution: bool = False):
        if not bool(self.kill_vote_list):
            await self.channel_list['m_chat'].send('투표자가 없습니다. 투표를 넘깁니다. ')
            return

        vote = {}
        for key, value in self.kill_vote_list.items():
            if vote.get(value):
                vote[value] += 1
            else:
                vote[value] = 1

        max_list = [k for k, v in vote.items() if max(vote.values()) == v]

        channel = ("g_chat" if is_execution else "m_chat")
        text = ("처형" if is_execution else "사살")
        if len(max_list) > 1:
            await self.channel_list[channel].send(f'{text} 대상이 결정되지 않았습니다.')
        elif max_list[0] is not self.revive_member:
            self.kill_member = max_list[0]
            await self.channel_list[channel].send(f'{self.kill_member.name} 을 {text} 합니다.')
            print(f'[마피아게임] {self.kill_member.name}가 {text}됨')

    # 사살 목표 투표 목록 보내기
    async def send_kill_vote_list(self):
        vote_list = ''
        for key, value in self.kill_vote_list.items():
            vote_list += f'{key} - {value}\n'

        _embed = discord.Embed(title='마피아게임', description=vote_list, color=0x00ff00)
        await self.channel_list['m_chat'].send(embed=_embed)

    # 소생할 유저 선택
    async def revive_user(self, ctx, name):
        print(f'[마피아게임] {ctx.author.name} - 치료')
        if self.members.get(name) is None:
            await self.channel_list['d_chat'].send('없는 유저 입니다.')
        elif ctx.channel is self.channel_list['d_chat']:
            self.revive_member = self.members[name][0]
            await self.channel_list['d_chat'].send(f'살릴사람: {name}')
            print(f'[마피아게임] {ctx.author.name}가 {name}을 치료함')

    # 유저 직업 조사
    async def user_research(self, ctx, name):
        if self.members.get(name) is None:
            await self.channel_list['p_chat'].send('없는 유저 입니다.')
        elif not self.can_search:
            await self.channel_list['p_chat'].send('더이상 조사할 수 없습니다.')
        elif ctx.channel is self.channel_list['p_chat']:
            await self.channel_list['p_chat'].send(f'{name}의 직업: {self.members[name][1]}')
            self.can_search = False
            print(f'[마피아게임] {ctx.author.name}가 {name}을 조사함')

    # 죽은 유저 유령으로 변경
    async def change_ghost(self):
        if self.kill_member is not None:
            self.members[self.kill_member.name] = (self.kill_member, '유령')
            await self.kill_member.edit(mute=True)
            print(f'[마피아게임] {self.kill_member.name}가 유령으로 변경됨')

    # channel 에 유저목록 보내기
    async def user_list(self, channel: discord.TextChannel):
        users = '유저목록\n'
        for i, member in enumerate(self.channel_list['g_voice'].members):
            users += f'{i}.{member.name}\n'
        _embed = discord.Embed(title='마피아게임', description=users, color=0x00ff00)
        await channel.send(embed=_embed)

    # 개인 메세지 보내기
    async def send_dm(self, member: discord.Member, text: str):
        _embed = discord.Embed(title='마피아게임', description=text, color=0x00ff00)
        if member.dm_channel:
            await member.dm_channel.send(embed=_embed)
        elif member.dm_channel is None:
            channel = await member.create_dm()
            await channel.send(embed=_embed)

    # 게임 종료
    async def end_game(self, ctx):
        if self.channel_list.get('category') is None:
            await ctx.send('게임이 시작되지 않았습니다.')
            return

        print(f'[마피아게임] ========== 게임 종료 ==========')

        for ch_key, ch in self.channel_list.items():
            await ch.delete()

        self.__init__(self.bot)

    # 유저 음성채널 이동
    async def connect_user_voice(self, member: discord.Member, channel: discord.VoiceChannel):
        if member.voice is not None:
            await member.move_to(channel)
            print(f'[마피아게임] {member.name}을 {channel.name}으로 이동시킴')

    # 채널 생성
    async def create_channel(self, ctx, name: str, _type: discord.ChannelType, category: discord.CategoryChannel = None, can_read: bool = True, can_send=True):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=can_read, send_messages=can_send),
            self.bot.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        print(f'[마피아게임] {category}에 속한 {name} {_type}채널이 [읽기: {can_read}  쓰기: {can_send}] 권한으로 생성됨')

        if _type == discord.ChannelType.text:
            return await ctx.guild.create_text_channel(name, category=category, overwrites=overwrites)
        elif _type == discord.ChannelType.voice:
            return await ctx.guild.create_voice_channel(name, category=category, overwrites=overwrites)
        elif _type == discord.ChannelType.category:
            return await ctx.guild.create_category(name)

    # 투표채널 활성화/비활성화
    async def set_active_execution_vote(self, active: bool, send_message: str = "", send_user_list: bool = False):
        for name, value in self.members.items():
            if value[1] == '유령':
                continue
            if send_user_list:
                await self.user_list(self.channel_list[f'{name}_vote'])
            if send_message != "":
                await self.channel_list[f'{name}_vote'].send(send_message)
            await self.set_channel_permissions(value[0], self.channel_list[f'{name}_vote'], can_read=active, can_send=active)
            print(f'[마피아게임] 처형 투표 채널 활성화됨')

    # 직업채널 활성화/비활성화
    async def set_active_role_channel(self, active: bool):
        for member in self.members.values():
            if member[1] == '마피아':
                await self.set_channel_permissions(member[0], self.channel_list['m_chat'], can_send=active)
            elif member[1] == '의사':
                await self.set_channel_permissions(member[0], self.channel_list['d_chat'], can_send=active)
            elif member[1] == '경찰':
                await self.set_channel_permissions(member[0], self.channel_list['p_chat'], can_send=active)
                print(f'[마피아게임] 직업채널 활성화됨')

    # 직업채널 투표 시작
    async def start_vote_role_channel(self):
        print(f'[마피아게임] 직업채널 투표 시작됨')

        # 마피아 채널에서 사살 투표
        await self.user_list(self.channel_list['m_chat'])
        await self.channel_list['m_chat'].send(
            f'사살할 유저를 투표해주세요.\n 투표는 25초간 진행됩니다.\n!{prefix} 사살 <유저이름> 으로 사살할 유저를 투표할 수 있습니다.')

        # 의사 채널에서 치료할 사람 투표
        await self.user_list(self.channel_list['d_chat'])
        await self.channel_list['d_chat'].send(
            f'치료할 유저를 투표해주세요.\n 투표는 25초간 진행됩니다.\n!{prefix} 치료 <유저이름> 으로 치료할 유저를 선택할 수 있습니다.')

        # 경찰 채널에서 치료할 사람 투표
        await self.user_list(self.channel_list['p_chat'])
        await self.channel_list['p_chat'].send(
            f'조사할 유저를 투표해주세요.\n 투표는 25초간 진행됩니다.\n!{prefix} 조사 <유저이름> 으로 조사할 유저를 선택할 수 있습니다.')

    # 모든 유저 음성 뮤트/뮤트 해제
    async def all_voice_mute(self, is_mute: bool):
        for member in self.channel_list['g_voice'].members:
            if member == self.bot.user:
                continue
            try:
                await member.edit(mute=is_mute)
            except discord.errors.HTTPException:
                continue
        print(f'[마피아게임] 모든 유저 음성 {"뮤트" if is_mute else "뮤트해제"}됨')

    # 모든 유저 채팅 뮤트/뮤트 해제
    async def all_chat_mute(self, channel: discord.TextChannel, can_send: bool):
        for member in channel.members:
            if member == self.bot.user:
                continue
            await self.set_channel_permissions(member, channel, can_send=can_send)
        print(f'[마피아게임] 모든 유저 {channel.name} 채팅 {"뮤트" if can_send else "뮤트해제"}됨')

    # 채널 권한 설정
    async def set_channel_permissions(self, member: discord.Member, channel, can_read: bool = True, can_send: bool = True):
        perms = channel.overwrites_for(member)
        perms.read_messages = can_read
        perms.send_messages = can_send
        await channel.set_permissions(member, overwrite=perms)
        print(f'[마피아게임] {channel.name} 채널의 {member}의 권한이 [읽기: {can_read}  쓰기: {can_send}] 으로 변경됨')
