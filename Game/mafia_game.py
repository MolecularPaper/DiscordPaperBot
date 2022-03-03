import asyncio
import discord
import random
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
        self.citizen = []
        self.mafia = []
        self.doctor = None

        # 채널 관련
        self.category = None
        self.lobby = None
        self.global_chat_channel = None
        self.mafia_chat_channel = None
        self.doctor_chat_channel = None
        self.global_voice_channel = None

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

    # 게임 시작
    async def start_game(self, ctx):
        if self.category is not None:
            await ctx.send('이미 게임이 진행중입니다.')
            return

        self.category = await self.create_category(ctx, '마피아게임')
        self.lobby = await self.create_voice_channel(ctx, '마피아게임-대기', True)
        self.global_chat_channel = await self.create_chat_channel(ctx, '마피아게임-공용-채팅', False)
        self.mafia_chat_channel = await self.create_chat_channel(ctx, '마피아게임-마피아-채팅', False)
        self.doctor_chat_channel = await self.create_chat_channel(ctx, '마피아게임-의사-채팅', False)
        self.global_voice_channel = await self.create_voice_channel(ctx, '마피아게임-음성', False)
        # await self.send_role(ctx, '테스트')

    # 게임참가 대기
    async def waiting_join(self, ctx):
        _embed = discord.Embed(title='마피아게임', description='게임에 참여할려면 마피아게임-대기 채널에 참가해주세요.'
                                                          '\n게임을 하기 위해서는 최소 5명 이상의 인원이 필요합니다.'
                                                          '\n게임은 20초 후에 시작되며, 이후 진행 상황은 마피아게임-공용-채팅에 나타납니다.'
                               , color=0x00ff00)
        await ctx.send(embed=_embed)
        await asyncio.sleep(20)

        self.citizen = self.lobby.members
        if len(self.citizen) >= 4:
            await self.global_chat_channel.send('게임을 시작합니다.')
            for member in self.citizen:
                await self.connect_user_voice(member)
                await self.set_visible_permissions(member, self.global_chat_channel, True)
            await self.lobby.delete()
            return True
        else:
            await ctx.send('인원이 부족하므로 게임을 중단합니다.')
            await asyncio.sleep(2)
            await self.lobby.delete()
            await self.end_game(ctx)
            return False

    # 역할 지정
    async def assign_role(self):
        await self.global_chat_channel.send('역할을 지정합니다. 개인 메세지를 확인해주세요.')

        # 마피아 지정
        for x in range(2):
            choice = random.choice(self.citizen)
            self.citizen.remove(choice)
            self.mafia.append(choice)
            await self.send_dm(choice, f'당신의 역할은 마피아 입니다.')
            await self.set_visible_permissions(choice, self.mafia_chat_channel, True)

        # 의사 지정
        choice = random.choice(self.citizen)
        self.citizen.remove(choice)
        self.doctor = choice
        await self.send_dm(choice, f'당신의 역할은 의사 입니다.')
        await self.set_visible_permissions(choice, self.doctor_chat_channel, True)

        for _citizen in self.citizen:
            await self.send_dm(_citizen, '당신의 역할은 시민입니다.')

        await asyncio.sleep(8)

    # 루프 관리
    async def loop(self):
        await self.night()
        await self.day()

    # 밤 진행
    async def night(self):
        self.is_day = False
        # 메세지 전송후 채널내 모든유저 뮤트
        await self.global_chat_channel.send('밤이 되었습니다...')
        await self.all_voice_mute(True)
        await self.all_chat_mute(self.global_chat_channel, True)

        # 마피아,의사 채팅 활성화
        for mafia in self.mafia:
            await self.set_send_permissions(mafia, self.mafia_chat_channel, True)
        await self.set_send_permissions(self.doctor, self.mafia_chat_channel, True)

        # 마피아 채널에서 사살 투표
        await self.user_list(self.mafia_chat_channel)
        await self.mafia_chat_channel.send('사살할 유저를 투표해주세요.\n 투표는 25초간 진행됩니다.')

        # 의사 채널에서 치료할 사람 투표
        await self.user_list(self.doctor_chat_channel)
        await self.mafia_chat_channel.send('치료할 유저를 투표해주세요.\n 투표는 25초간 진행됩니다.')

        # 25초간 대기
        await asyncio.sleep(25)

        # 판정
        await self.kill_user()
        self.is_day = True

        return

    # 낮 진행
    async def day(self):
        # 메세지 전송후 채널내 모든유저 뮤트 해제
        await self.global_chat_channel.send('낮이 되었습니다.')
        await self.all_voice_mute(False)
        await self.all_chat_mute(self.global_chat_channel, False)

        # 마피아,의사 채팅 비활성화
        for mafia in self.mafia:
            await self.set_send_permissions(mafia, self.mafia_chat_channel, False)
        await self.set_send_permissions(self.doctor, self.mafia_chat_channel, False)

        # 사살된 사람 알림
        if self.kill_member is not None:
            await self.mafia_chat_channel.send(f'{self.kill_member.name} 가 사망하였습니다.')
            await self.kill_member.edit(mute=True)
            await self.set_send_permissions(self.kill_member, self.global_chat_channel, False)
            await self.set_send_permissions(self.kill_member, self.doctor_chat_channel, False)
            await self.set_send_permissions(self.kill_member, self.mafia_chat_channel, False)

        return

    # 사살 투표
    async def kill_vote(self, ctx, name):
        if ctx.channel is self.mafia_chat_channel:
            member = self.get_member(name)
            if member is not None:
                if self.kill_vote_list.get(member):
                    self.kill_vote_list[member] += 1
                else:
                    self.kill_vote_list[member] = 1

    # 사살 목표 확정
    async def kill_user(self):
        if not bool(self.kill_vote_list):
            await self.mafia_chat_channel.send('투표자가 없습니다. 투표를 넘깁니다. ')
            return

        max = max(self.kill_vote_list.values())
        list = []
        for elements in self.kill_vote_list:
            for key, value in self.kill_vote_list.items():
                if value == max:
                    list.append(key)

        if len(list) > 1:
            await self.mafia_chat_channel.send('사살 목표가 결정되지 않았습니다. 투표를 넘깁니다. ')
        else:
            self.kill_member = list[0]
            print(list[0])
            await self.mafia_chat_channel.send(f'{self.kill_member.name} 을 사살합니다.')

    # 소생할 유저 선택
    async def revive_user(self, ctx, name):
        if ctx.channel is self.doctor_chat_channel:
            if self.revive_member is None:
                self.revive_member = self.get_member(name)
                self.doctor_chat_channel.send(f'살릴사람: {name}')

    async def get_member(self, name):
        for member in self.global_voice_channel.members:
            if member.name is name:
                return member

    # channel 에 유저목록 보내기
    async def user_list(self, channel: discord.TextChannel):
        users = '유저목록\n'
        for member in self.global_voice_channel.members:
            users += f'1.{member.name}\n'
        _embed = discord.Embed(title='마피아게임', description=users, color=0x00ff00)
        await channel.send(embed=_embed)

    # 모든 유저 음성 뮤트/뮤트 해제
    async def all_voice_mute(self, is_mute: bool):
        for member in self.global_voice_channel.members:
            await member.edit(mute=is_mute)

    # 모든 유저 채팅 뮤트/뮤트 해제
    async def all_chat_mute(self, channel: discord.TextChannel, is_mute: bool):
        for member in self.global_voice_channel.members:
            await self.set_send_permissions(member, channel, not is_mute)

    # 권한 설정 - 채널 보이기
    async def set_visible_permissions(self, member: discord.Member, channel, visible):
        perms = channel.overwrites_for(member)
        perms.read_messages = visible
        await channel.set_permissions(member, overwrite=perms)

    # 권한 설정 - 채널 채팅 보내기
    async def set_send_permissions(self, member: discord.Member, channel, can_send):
        perms = channel.overwrites_for(member)
        perms.send_messages = can_send
        await channel.set_permissions(member, overwrite=perms)

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
        if self.category is None:
            await ctx.send('게임이 시작되지 않았습니다.')
            return

        await self.all_voice_mute(False)
        await self.global_chat_channel.delete()
        await self.mafia_chat_channel.delete()
        await self.doctor_chat_channel.delete()
        await self.global_voice_channel.delete()
        await self.category.delete()

        self.__init__(self.bot)

    # 유저 음성채널 이동
    async def connect_user_voice(self, member: discord.Member):
        if member.voice is not None:
            await member.move_to(self.global_voice_channel)

    # 카테고리 생성
    async def create_category(self, ctx, name: str):
        guild = ctx.message.guild
        return await ctx.guild.create_category(name)

    # 채팅채널 생성
    async def create_chat_channel(self, ctx, name: str, visible: bool):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=visible, send_messages=visible),
            self.bot.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        return await ctx.guild.create_text_channel(name, category=self.category, overwrites=overwrites)

    # 음성채널 생성
    async def create_voice_channel(self, ctx, name: str, visible: bool):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=visible),
            self.bot.user: discord.PermissionOverwrite(read_messages=True),
        }
        return await ctx.guild.create_voice_channel(name, category=self.category, overwrites=overwrites)
