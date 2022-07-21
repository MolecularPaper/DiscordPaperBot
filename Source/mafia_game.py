from distutils.command.config import config
from click import command
import discord, asyncio, json, utility
from multiprocessing.dummy import Array
from discord.ext import commands

config_path = './Data/Mafia/mafia_game_config.json'
text_path = './Data/Mafia/mafia_text.json'
channel_path = './Data/Mafia/mafia_channel.json'
trigger_path = './Data/Mafia/mafia_game_val.txt'

class Mafia(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.config = self.ReadJson(config_path) #게임 기본 옵션 설정 (변경 가능)
        self.systext = self.ReadJson(text_path) #게임 텍스트 설정
        self.channels = self.ReadJson(channel_path) #게임 채널 설정
        self.game_value = self.ReadJson(trigger_path) #게임 내부 트리거 설정

        global prefix
        prefix = self.config['prefix']

        self.CreateChannel()
    
    def ReadCommand(func, self, ctx, command, name=''):
        def wrapper():
            if command == name:
                func(self, ctx)
        return wrapper

    @commands.command(name=prefix)
    @ReadCommand(name='매치생성')
    async def Match(self, ctx):
        await self.SendText(ctx, self.ConvertText(self.systext['match_making']['start']))

    @commands.command(name=prefix)
    @ReadCommand(name='매치중단')
    async def MatchStop(self, ctx):
        await self.SendText(ctx, self.systext['match_making']['stop'])
        del self
        
    @commands.command(name=prefix)
    @ReadCommand(name='게임시작')
    async def GameStart(self, ctx):
        #유저수 검사후 시작 가능하면 시작
        await self.SendText(ctx, self.systext['match_making']['start'])
        return

    commands.command(name=prefix)
    @ReadCommand(name='게임 종료')
    async def GameStop(self, ctx):
        await self.SendText(ctx, self.systext['match_making']['stop'])
        del self

    async def ReadJson(self, path) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    async def CreateChannel(self, ctx):
        for channel in self.channels.values():
            self.channels[channel] = await utility.create_channel(ctx, channel['name'], channel['type'])

    async def SendText(self, channel, text:str):
        await channel.send(text)

    async def WaitTimeSceond(self, pointer:str, callback=None):
        await asyncio.sleep(self.config[pointer])
        if callback is not None:
            callback()

    def ConvertText(self, text: str) -> str:
        for key, value in self.config.items():
            text = self.ReplaceText(text, key, value)
        for key, value in self.channels.items():
            text = self.ReplaceText(text, key, value['name'])
        return text

    def ReplaceText(self, text: str, key: str, value):
        return text.replace('{' + key + '}', str(value))

async def cancel_me():
     while True:
        await asyncio.sleep(3600)
        print("cancel me plz")

def wrapped_coroutine():
     for task in asyncio.all_tasks():
         try:
             task.cancel()
         except asyncio.CancelledError:
             print("Task cancelled")