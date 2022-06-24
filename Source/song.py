import discord, youtube_dl, json, time
from matplotlib.pyplot import title
from discord.ext import commands
import asyncio

class Song(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_list = []
    
    @commands.command(name='연결')
    async def join(self, ctx):
        voice = ctx.message.author.voice
        voice_client = ctx.guild.voice_client
        # 유저가 음성채널에 연결되어있는지 확인
        if voice and voice.channel:
            # 봇이 음성채널에 연결되어 있는지 확인
            if voice_client and voice_client.is_connected():
                # 봇이 유저랑 같은 음성 채널에 있는지 확인
                if voice_client.channel == voice.channel:
                    await ctx.send('이미 연결되어 있습니다.')
                else:
                    # 현재 채널에서 나간 후 유저가 있는 채널로 재연결
                    await voice_client.disconnect()
                    await voice.channel.connect()
            else:
                await voice.channel.connect()
        else:
            await ctx.send('먼저 음성채널에 연결해주세요')

    @commands.command(name='재생')
    async def play(self, ctx, url: str):
        voice = ctx.message.author.voice
        voice_client = ctx.guild.voice_client
        # 유저가 음성채널에 연결되어있는지 확인
        if voice and voice.channel:
            # 봇이 음성채널에 연결되어있지 않다면 유저가 있는 채널에 연결함
            if not (voice_client and voice_client.is_connected()):
                await voice.channel.connect()

        # 유튜브 다운로더 옵션 로딩
        with open('Data/ydl_opts.json', 'r') as f:
                ydl_opts = json.load(f)
        
        # URL 등록
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            title = info['title']
            length = info['duration']

            self.song_list.append((URL, title, length))
            await ctx.send(f'재생목록에 추가됨: {title}')
        
        await self.play_song(ctx)
    
    # 음악 재생
    async def play_song(self, ctx):
        #ffmpeg 옵션 로딩
        with open('Data/ffmpeg_options.json', 'r') as f:
            ffmpeg_options = json.load(f)
        
        # 이미 재생 중이라면 리턴
        if self.bot.voice_clients[0].is_playing():
            return
        
        await ctx.send(f'지금 재생중: {self.song_list[0][1]}')
        source = discord.FFmpegPCMAudio(self.song_list[0][0], **ffmpeg_options, executable='ffmpeg/bin/ffmpeg.exe')
        self.bot.voice_clients[0].play(source, after=lambda e: self.next_song(ctx))
    
    # 다음곡 재생
    def next_song(self, ctx):
        self.song_list.pop()
        if len(self.song_list) == 0:
            return
        asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.bot.loop)

    @commands.command(name='연결해제')
    async def leave(self, ctx):
        voice_client = ctx.guild.voice_client
        # 봇이 음성채널에 연결되어있는지 확인
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send('음성채널에 연결되어있지 않습니다')

    @commands.command(name='재생목록')
    async def play_list(self, ctx):
        list = ""
        for i, song in enumerate(self.song_list):
            time = song[2]
            hour = int(time / 3600) # 시 공식
            minute = int(time % 3600 / 60); # 분을 구하기위해서 입력되고 남은값에서 또 60을 나눈다.
            second = int(time % 3600 % 60); # 마지막 남은 시간에서 분을 뺀 나머지 시간을 초로 계산함
            list += f'{i + 1}. {song[1]} [{hour}:{minute}:{second}]\n'
        await ctx.send(list)