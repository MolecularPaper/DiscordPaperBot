import asyncio
import discord

from discord.ext import commands

def read_file(filename):
        file = open(f'./Data/{filename}.txt', 'r', encoding="UTF-8").readlines()
        file_text = ""
        for line in file:
            file_text += line
        return file_text

async def send_edit(channel, msg, edit_msg, delay):
    '''메세지 전송후 dleay시간 만큼 대기후 edit_msg로 수정'''
    tk = await channel.send(msg)
    await asyncio.sleep(delay)
    await tk.edit(content=edit_msg)

async def create_channel(ctx, bot, name: str, _type: str, category: discord.CategoryChannel = None, can_read: bool = True, can_send=True, print_log=True):
    '''채널 생성 (채널이 있는경우, 그 채널 반환)'''
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=can_read, send_messages=can_send),
        bot.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    if print_log:
        print(f'[INFO] {category}에 속한 {name} {_type}채널이 [읽기: {can_read}  쓰기: {can_send}] 권한으로 생성됨')

    for channel in ctx.guild.channels:
        if channel.name == name:
            return channel
    
    if _type == "text":
        return await ctx.guild.create_text_channel(name, category=category, overwrites=overwrites)
    elif _type == "voice":
        return await ctx.guild.create_voice_channel(name, category=category, overwrites=overwrites)
    elif _type == "category":
        return await ctx.guild.create_category(name)
    

async def set_user_permissions(member: discord.Member, channel, can_read: bool = True, can_send: bool = True, print_log=True):
    '''채널 권한 설정'''
    perms = channel.overwrites_for(member)
    perms.read_messages = can_read
    perms.send_messages = can_send
    await channel.set_permissions(member, overwrite=perms)
    
    if print_log:
        print(f'[INFO] {channel.name} 채널의 {member}의 권한이 [읽기: {can_read}  쓰기: {can_send}] 으로 변경됨')

async def set_channel_permission(ctx, channel, can_read:bool, can_send:bool):
    set_user_permissions(ctx.guild.default_role, channel, can_read, can_send)

async def dm_channel(member: discord.Member):
    '''DM 채널 반환 (없을경우 생성함)'''
    channel = member.dm_channel
    if channel is None:
        await member.create_dm()
    return channel

async def send_dm_embed(member: discord.Member, title:str, text: str, color=0x00ff00):
    '''개인 메세지 보내기 (임베드)'''
    _embed = discord.Embed(title=title, description=text, color=color)
    channel = dm_channel(member)
    await channel.send(embed=_embed)

async def send_dm(member: discord.Member, text: str):
    '''개인 메세지 보내기'''
    channel = dm_channel(member)
    await channel.send(text)

async def connect_user_voice(member: discord.Member, channel: discord.VoiceChannel):
    '''유저 음성채널 이동'''
    if member.voice is not None:
        await member.move_to(channel)
        print(f'[INFO] {member.name}을 {channel.name}으로 이동시킴')

async def connect_all_user_voice(members, channel: discord.VoiceChannel):
    '''유저 음성채널 이동'''
    for member in members:
        await connect_user_voice(member, channel)