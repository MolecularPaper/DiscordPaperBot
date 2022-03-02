from typing import Any

import discord, asyncio
from discord.ext import commands


class Mafia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx = Any
        self.members = Any
        self.category = Any
        self.lobby = Any
        self.global_chat_channel = Any
        self.mafia_chat_channel = Any
        self.global_voice_channel = Any

    # 봇 정보
    @commands.command(name='마피아게임')
    async def read_command(self, ctx, args):
        self.ctx = ctx
        if args == '시작':
            await self.start_game()
        elif args == '종료':
            await self.end_game()

    async def start_game(self):
        if not self.category == Any:
            await self.ctx.send('이미 게임이 시작되었습니다.')
            return

        self.category = await self.create_category('마피아게임')
        self.lobby = await self.create_voice_channel('마피아게임-대기', True)
        self.global_chat_channel = await self.create_chat_channel('마피아게임-공용-채팅', False)
        self.mafia_chat_channel = await self.create_chat_channel('마피아게임-마피아-채팅', False)
        self.global_voice_channel = await self.create_voice_channel('마피아게임-음성', False)

        await self.connet_user_voice(self.ctx.author)
        await self.ctx.send('게임에 참여할려면 마피아게임-대기 채널에 참가해주세요.\n게임을 하기 위해서는 최소 5명 이상의 인원이 필요합니다.\n게임은 10초 후에 시작되며, 이후 진행 상황은 마피아게임-공용-채팅에 나타납니다.')
        await asyncio.sleep(10)

        self.members = self.lobby.members
        await self.global_chat_channel.send('게임을 시작합니다.')
        for member in members:
            await self.connet_user_voice(member)
        return

        if len(self.members) > 5:
            await self.global_chat_channel.send('게임을 시작합니다.')
            for member in self.members:
                await self.connet_user_voice(member)
        else:
            await self.global_chat_channel.send('인원이 부족하기 때문에 게임을 중단합니다.')
            await asyncio.sleep(2)
            await self.end_game()

        # await self.send_role(self.ctx, '테스트')

    async def end_game(self):
        if self.category == Any:
            await self.ctx.send('게임이 시작되지 않았습니다.')
            return

        await self.lobby.delete()
        await self.global_chat_channel.delete()
        await self.mafia_chat_channel.delete()
        await self.global_voice_channel.delete()
        await self.category.delete()

        self.members = Any
        self.category = Any
        self.lobby = Any
        self.global_chat_channel = Any
        self.mafia_chat_channel = Any
        self.global_voice_channel = Any

    async def connet_user_voice(self, member):
        if member.voice != None:
            await member.move_to(self.global_voice_channel)



    async def create_category(self, name):
        guild = self.ctx.message.guild
        return await self.ctx.guild.create_category(name)

    async def create_chat_channel(self, name, visible):
        overwrites = {
            self.ctx.guild.default_role: discord.PermissionOverwrite(read_messages=visible),
            self.bot.user: discord.PermissionOverwrite(read_messages=True)
        }
        return await self.ctx.guild.create_text_channel(name, category=self.category, overwrites=overwrites)

    async def create_voice_channel(self, name, visible):
        overwrites = {
            self.ctx.guild.default_role: discord.PermissionOverwrite(read_messages=visible),
            self.bot.user: discord.PermissionOverwrite(read_messages=True)
        }
        return await self.ctx.guild.create_voice_channel(name, category=self.category, overwrites=overwrites)

    async def send_role(self, role):
        _embed = discord.Embed(title='마피아게임', description=f'당신의 역할: {role}', color=0x00ff00)

        if self.ctx.author.dm_channel:
            await self.ctx.author.dm_channel.send(embed=_embed)
        elif self.ctx.author.dm_channel is None:
            channel = await ctx.author.create_dm()
            await channel.send(embed=_embed)
