import discord, asyncio, json, utility
from multiprocessing.dummy import Array
from discord.ext import commands

config_path = './Data/Mafia/mafia_game_config.json'
text_path = './Data/Mafia/mafia_text.json'
channel_path = './Data/Mafia/mafia_channel.json'
trigger_path = './Data/Mafia/mafia_game_trigger.txt'

class MafiaCommand(commands.Cog):
    def __init__(self, bot) -> None:
        self.mafia = None
        self.bot = bot
        
    def ReadCommand(self, ctx, command, arg):
        return

class Mafia(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.config = self.ReadJson(config_path) #게임 기본 옵션 설정 (변경 가능)
        self.systext = self.ReadJson(text_path) #게임 텍스트 설정
        self.channels = self.ReadJson(channel_path) #게임 채널 설정
        self.triggers = self.ReadJson(trigger_path) #게임 내부 트리거 설정
        
        self.CreateChannel()

    async def ReadJson(self, path) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    async def CreateChannel(self, ctx):
        for channel in self.channels.keys():
            self.channels[channel] = await self.create_channel(ctx, '마피아게임', discord.ChannelType.category)
        return
    
    async def Match(self, ctx):
        await self.SendText(ctx, self.ConvertText(self.systext['match_making']['start']))

    async def MatchStop(self, ctx):
        await self.SendText(ctx, self.systext['match_making']['stop'])
        del self

    async def GameStart(self, ctx):
        #유저수 검사후 시작 가능하면 시작
        await self.SendText(ctx, self.systext['match_making']['start'])
        return

    async def GameStop(self, ctx):
        await self.SendText(ctx, self.systext['match_making']['stop'])
        del self

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
            text = self.ReplaceText(text, key, value)
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

if __name__ == "__main__":
    bot = commands.Bot(command_prefix='테스트')
    mafia = Mafia(bot)
    
    cancel_me()
    wrapped_coroutine()