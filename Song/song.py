import discord, youtube_dl, json, time
from discord.ext import commands


class Song(commands.Cog):
    def __init__(self, bot):
        bot.remove_command("help")
        self.bot = bot

    @commands.command(name='join')
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

    @commands.command(name='play')
    async def play(self, ctx, url: str):
        voice = ctx.message.author.voice
        voice_client = ctx.guild.voice_client
        # 유저가 음성채널에 연결되어있는지 확인
        if voice and voice.channel:
            # 봇이 음성채널에 연결되어있지 않다면 유저가 있는 채널에 연결함
            if not (voice_client and voice_client.is_connected()):
                await voice.channel.connect()
            with open('Options/ydl_opts.json', 'r') as f:
                ydl_opts = json.load(f)
            with open('Options/ffmpeg_options.json', 'r') as f:
                ffmpeg_options = json.load(f)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
            self.bot.voice_clients[0].play(discord.FFmpegPCMAudio(URL, **ffmpeg_options, executable='ffmpeg/bin/ffmpeg.exe'))

    @commands.command(name='leave')
    async def leave(self, ctx):
        voice_client = ctx.guild.voice_client
        # 봇이 음성채널에 연결되어있는지 확인
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send('음성채널에 연결되어있지 않습니다')
