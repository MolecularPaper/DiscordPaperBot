import asyncio
import discord
import random

import self as self
from discord.ext import commands


class Mafia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 변수
        self.is_day = False
        self.revive_member = None
        self.kill_member = None
        self.kill_vote_list = {}

        # 맴버
        self.members = {}

        # 채널 관련
        self.channel_list = {}
    # 게임 명령어
    @commands.command(name='마피아게임')
    async def read_command(self, ctx, *args):
        if args[0] == '시작':
            await self.start_game(ctx)
            can_start = await self.waiting_join(ctx)
            if can_start:
                await self.assign_role()
            await self.loop()
        elif args[0] == '종료':
            await self.end_game(ctx)
        elif args[0] == '사살':
            await self.kill_vote(ctx, args[1])
        elif args[0] == '치료':
            await self.revive_member(ctx, args[1])

    # 게임 시작
    async def start_game(self, ctx):
        if bool(self.channel_list):
            await ctx.send('이미 게임이 진행중입니다.')
            return

        self.channel_list['category'] = await self.create_channel(ctx, '마피아게임', discord.ChannelType.category)
        self.channel_list['lobby'] = await self.create_channel(ctx, '대기', discord.ChannelType.voice, category=self.channel_list['category'])
        self.channel_list['ghost'] = await self.create_channel(ctx, '유령', discord.ChannelType.voice, category=self.channel_list['category'], can_read=False, can_send=False)
        self.channel_list['g_voice'] = await self.create_channel(ctx, '음성', discord.ChannelType.voice, category=self.channel_list['category'], can_read=False, can_send=False)
        self.channel_list['g_chat'] = await self.create_channel(ctx, '공용', discord.ChannelType.text, category=self.channel_list['category'], can_read=False, can_send=False)
        self.channel_list['m_chat'] = await self.create_channel(ctx, '마피아', discord.ChannelType.text, category=self.channel_list['category'], can_read=False, can_send=False)
        self.channel_list['d_chat'] = await self.create_channel(ctx, '의사', discord.ChannelType.text, category=self.channel_list['category'], can_read=False, can_send=False)
        # await self.send_role(ctx, '테스트')

    # 게임참가 대기
    async def waiting_join(self, ctx):
        _embed = discord.Embed(title='마피아게임', description='게임에 참여할려면 마피아게임-대기 채널에 참가해주세요.'
                                                          '\n게임을 하기 위해서는 최소 4명 이상의 인원이 필요합니다.'
                                                          '\n게임은 20초 후에 시작되며, 이후 진행 상황은 마피아게임-공용-채팅에 나타납니다.'
                               , color=0x00ff00)
        await ctx.send(embed=_embed)
        await asyncio.sleep(20)

        members = self.channel_list['g_voice'].members
        if len(members) >= 3:
            await self.channel_list['g_chat'].send('게임을 시작합니다.')
            for member in members:
                await self.connect_user_voice(member, self.channel_list['g_voice'])
                await self.set_channel_permissions(member, self.channel_list['lobby'], False)
                await self.set_channel_permissions(member, self.channel_list['g_chat'])
            return True
        else:
            await ctx.send('인원이 부족하므로 게임을 중단합니다.')
            await asyncio.sleep(2)
            await self.end_game(ctx)
            return False

    # 밤 진행
    async def night(self):
        self.is_day = False
        # 메세지 전송후 채널내 모든유저 뮤트
        await self.channel_list['g_chat'].send('밤이 되었습니다...')
        await self.all_voice_mute(True)
        await self.all_chat_mute(self.channel_list['g_chat'], True)

        # 마피아,의사 채팅 활성화
        self.set_active_role_channel(True)

        # 마피아 채널에서 사살 투표
        await self.user_list(self.channel_list['m_chat'])
        await self.channel_list['m_chat'].send('사살할 유저를 투표해주세요.\n 투표는 25초간 진행됩니다.')

        # 의사 채널에서 치료할 사람 투표
        await self.user_list(self.channel_list['d_chat'])
        await self.channel_list['d_chat'].send('치료할 유저를 투표해주세요.\n 투표는 25초간 진행됩니다.')

        # 25초간 대기
        await asyncio.sleep(25)

        # 판정
        await self.kill_user()
        self.is_day = True
        return

    # 낮 진행
    async def day(self):
        # 메세지 전송후 채널내 모든유저 뮤트 해제
        await self.channel_list['g_chat'].send('낮이 되었습니다.')
        await self.all_voice_mute(False)
        await self.all_chat_mute(self.channel_list['g_chat'], False)

        # 직업채널 비활성화
        self.set_active_role_channel(False)

        # 밤에 일어난일 설명
        if self.kill_member is not None and self.kill_member.name != self.revive_member:
            await self.change_ghost(self.kill_member)
        else:
            await self.channel_list['g_chat'].send('아무일도 일어나지 않았습니다...')

        self.kill_member = None
        self.kill_vote_list = {}

    # 역할 뽑기
    async def assign_role(self):
        await self.channel_list['g_chat'].send('역할을 지정합니다. 개인 메세지를 확인해주세요.')
        members = self.channel_list['g_voice'].members

        # 마피아 지정
        for x in range(2):
            choice = random.choice(members)
            await self.set_role(choice, '마피아')
            members.remove(choice)

        # 의사 지정
        choice = random.choice(members)
        await self.set_role(choice, '의사')
        members.remove(choice)

        for _citizen in self.citizen:
            await self.set_role(choice, '시민')

        await asyncio.sleep(8)

    # 역할 설정
    async def set_role(self, member, role: str):
        self.members[member.name] = ('member', member)
        await self.send_dm(member, f'당신의 역할은 {str} 입니다.')
        await self.set_channel_permissions(member, self.channel_list['m_chat'], can_send=False)

    # 낮/밤 루프
    async def loop(self):
        while True:
            await self.night()
            await self.day()

    # 게임 진행상황 확인
    async def check_game(self):
        return

    # 사살 투표
    async def kill_vote(self, ctx, name):
        if ctx.channel is self.channel_list['m_chat']:
            member = self.members[name]
            if member.name == name:
                if member in self.kill_vote_list:
                    self.kill_vote_list[member] += 1
                else:
                    self.kill_vote_list[member] = 1
                await self.send_kill_vote_list()
            else:
                await self.channel_list['m_chat'].send('없는 유저 입니다.')

    # 사살 목표 확정
    async def kill_user(self):
        if not bool(self.kill_vote_list):
            await self.channel_list['m_chat'].send('투표자가 없습니다. 투표를 넘깁니다. ')
            return

        max_list = [k for k, v in self.kill_vote_list.items() if max(self.kill_vote_list.values()) == v]
        print(max_list)

        if len(max_list) > 1:
            await self.channel_list['m_chat'].send('사살 목표가 결정되지 않았습니다. 투표를 넘깁니다. ')
        else:
            self.kill_member = max_list[0]
            await self.channel_list['m_chat'].send(f'{self.kill_member.name} 을 사살합니다.')

    # 사살 목표 투표 목록 보내기
    async def send_kill_vote_list(self):
        vote_list = ''
        for key, value in self.kill_vote_list.items():
            vote_list += f'{key} - {value}표\n'

        _embed = discord.Embed(title='마피아게임', description=vote_list, color=0x00ff00)
        await self.channel_list['m_chat'].send(embed=_embed)

    # 소생할 유저 선택
    async def revive_user(self, ctx, name):
        if ctx.channel is self.channel_list['d_chat']:
            if self.revive_member is None:
                self.revive_member = self.members[name][0]
                self.channel_list['d_chat'].send(f'살릴사람: {name}')

    # 사살된 사람 유령으로 변경
    async def change_ghost(self, member: discord.Member):
        await self.channel_list['g_chat'].send(f'<{member.name}> 가 사망하였습니다.')


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
        if self.channel_list['category'] is None:
            await ctx.send('게임이 시작되지 않았습니다.')
            return

        for element in self.channel_list.values():
            await element.delete()

        self.__init__(self.bot)

    # 유저 음성채널 이동
    async def connect_user_voice(self, member: discord.Member, channel: discord.VoiceChannel):
        if member.voice is not None:
            await member.move_to(channel)

    # 채널 생성
    async def create_channel(self, ctx, name: str, type: discord.ChannelType, category: discord.CategoryChannel = None,can_read: bool = True, can_send = True):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=can_read, send_messages=can_send),
            self.bot.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        if type == discord.ChannelType.text:
            return await ctx.guild.create_text_channel(name, category=category, overwrites=overwrites)
        elif type == discord.ChannelType.voice:
            return await ctx.guild.create_voice_channel(name, category=category, overwrites=overwrites)
        elif type == discord.ChannelType.category:
            return await ctx.guild.create_category(name)

    # 직업채널 활성화 & 비활성화
    async def set_active_role_channel(self, active):
        for member in self.members:
            if member[1] == '마피아':
                await self.set_channel_permissions(member, self.channel_list['m_chat'], can_send=active)
            elif member[1] == '의사':
                await self.set_channel_permissions(member, self.channel_list['d_chat'], can_send=active)

    # 모든 유저 음성 뮤트/뮤트 해제
    async def all_voice_mute(self, is_mute: bool):
        for member in self.channel_list['g_voice'].members:
            try:
                await member.edit(mute=is_mute)
            except discord.errors.HTTPException:
                continue

    # 모든 유저 채팅 뮤트/뮤트 해제
    async def all_chat_mute(self, channel: discord.TextChannel, can_send: bool):
        for member in channel.members:
            await self.set_channel_permissions(member, channel, can_send=can_send)

    # 채널 권한 설정
    async def set_channel_permissions(self, member: discord.Member, channel, visible: bool = True, can_send: bool = True):
        perms = channel.overwrites_for(member)
        perms.read_messages = visible
        perms.send_messages = can_send
        await channel.set_permissions(member, overwrite=perms)
