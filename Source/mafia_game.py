import discord, asyncio, random, json
from discord.ext import commands

config_path = './Data/Mafia/mafia_game_config.json'
text_path = './Data/Mafia/mafia_game_text.json'

class MafiaCommand(commands.Cog):
    def __init__(self, bot) -> None:
        self.mafia = None
        self.bot = bot
        
    def ReadCommand(self, ctx, command, arg):
        return

class Mafia(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        #게임 기본 옵션 설정 (변경 가능)
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        #게임 텍스트 설정
        with open(text_path, 'r', encoding='utf-8') as f:
            self.game_text = json.load(f)

    async def ExcuteMetod(method_name):
        await getattr(Mafia, method_name)()
        return

    async def SendText(self, channel, pointer:str):
        await channel.send(self.game_text[pointer])

    async def SendText(self, channel, message:str, change:str, value):
        await channel.send(message.replace(change, str(value)))

    async def WaitTimeSceond(self, pointer:str):
        await asyncio.sleep(self.config[pointer])

def ConvertText(text: str, config: json) -> str:
    return text

if __name__ == "__main__":
    bot = commands.Bot(command_prefix='테스트')
    mafia = Mafia(bot)