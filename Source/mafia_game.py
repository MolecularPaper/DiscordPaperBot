from asyncio import tasks
import discord, asyncio, json
from discord.ext import commands
from sqlalchemy import true
from Source import utility

config_path = './Data/Mafia/mafia_game_config.json'
text_path = './Data/Mafia/mafia_game_text.json'
channel_path = './Data/Mafia/mafia_game_channel.json'
trigger_path = './Data/Mafia/mafia_game_val.json'
player_path = './Data/Mafia/mafia_game_player.json'
prefix = '마피아'

class Player():
    def __init__(self):
        self.member = None
        self.role = ""
        self.is_dead = False
        return

    async def ChangeVoiceChannel(self, channel:discord.VoiceChannel):
        if self.member.voice is not None:
            await self.member.move_to(channel)
            print(f'[INFO] {self.member.name}을 {channel.name}으로 이동시킴')

class Mafia(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.config = self.ReadJson(config_path) #게임 기본 옵션 설정 (변경 가능)
        self.systext = self.ReadJson(text_path) #게임 텍스트 설정
        self.channels = self.ReadJson(channel_path) #게임 채널 설정
        self.game_value = self.ReadJson(trigger_path) #게임 내부 트리거 설정
        self.playes = []
        self.tasks = []
    
    # 캔슬 가능한 Task (데코레이터)
    def CancelableTask(func):
        async def wrapper(self, ctx, *args):
            task = asyncio.create_task(func(self, ctx, *args))
            self.tasks.append(task)
            try:
                await task
            except Exception as e:
                print(f"작업 취소됨: {e}")
            self.tasks.remove(task)
        return wrapper
    
    async def CancelAllTask(self):
        for task in self.tasks:
            task.cancel()
    
    # 매치를 생성함 
    @commands.command(name=prefix + '_매치생성')
    @CancelableTask
    async def Match(self, ctx):
        # 이미 매치가 진행중인지 확인
        if self.game_value['is_match']:
            await self.SendText(ctx, self.systext['error']['match_already_start'])
        
        await self.CreateChannel(ctx)
        await self.SendText(ctx, self.ConvertText(self.systext['match_making']['start']))
        self.game_value['is_match'] = True
    
    # 매치를 중단하고 게임을 종료시킴
    @commands.command(name=prefix + '_매치중단')
    @CancelableTask
    async def MatchStop(self, ctx):
        if not self.game_value['is_match']:
            await self.SendText(ctx, self.systext['error']['game_does_not_match'])
            return

        self.game_value['is_match'] = False
        await self.CancelAllTask()
        await self.SendText(ctx, self.systext['match_making']['stop'])
    
    # 게임을 시작함
    @commands.command(name=prefix + '_게임시작')
    @CancelableTask
    async def GameStart(self, ctx):
        # 매치가 진행중인지 확인
        if not self.game_value['is_match']:
            await self.SendText(ctx, self.systext['error']['none_game'])
            return
        
        # 이미 게임이 진행중인지 확인
        if self.game_value['is_start']:
            await self.SendText(ctx, self.systext['error']['game_already_start'])
            return
        
        # 매치중인 유저수 확인
        members = self.channels['match_making_channel']['channel'].members
        if len(members) < self.config['min_player_count']:
            await self.SendText(ctx, self.systext['error']['shortage_of_players'])
            return
        
        await self.SendText(ctx, self.systext['game']['start'])
        
        # 매칭중인 유저 게임 보이스 채널로 이동
        voice_channel = self.channels['voice_channel']['channel']
        await utility.connect_all_user_voice(members, voice_channel)
    
    # 진행중인 게임을 종료함
    @commands.command(name=prefix + '_게임종료')
    @CancelableTask
    async def GameStop(self, ctx):
        # 게임이 시작되었는지 확인
        if not self.game_value['is_start']:
            await self.SendText(ctx, self.systext['error']['game_does_not_start'])
            return

        self.game_value['is_start'] = False
        await self.CancelAllTask()
        await self.SendText(ctx, self.systext['game']['stop'])

    # Json 데이터 파싱
    def ReadJson(self, path) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 게임 채널 생성
    async def CreateChannel(self, ctx):
        for key, value in self.channels.items():
            category = self.channels.get('category').get('channel')
            self.channels[key]['channel'] = await utility.create_channel(ctx, self.bot, value['name'], value['type'], category)

    # 채널에 매세지 전송
    async def SendText(self, channel, text:str):
        await channel.send(text)

    # 설정한 시간만큼 대기후, callback 함수 실행
    async def WaitTimeSceond(self, pointer:str, callback=None):
        await asyncio.sleep(self.config[pointer])
        if callback is not None:
            callback()

    # Text의 변환 가능한 문자열을 찾고, 해당 값으로 변환시킴
    def ConvertText(self, text: str) -> str:
        for key, value in self.config.items():
            text = self.ReplaceText(text, key, value)
        for key, value in self.channels.items():
            text = self.ReplaceText(text, key, value['name'])
        return text

    # Text에 정의되어있는 변수목록을 해당하는 값으로 변환함
    def ReplaceText(self, text: str, key: str, value):
        return text.replace('{' + key + '}', str(value))