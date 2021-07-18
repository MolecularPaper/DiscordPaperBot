import asyncio

import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

playerlist = []


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='연결')
    async def join(self, ctx):
        """Joins a voice channel"""
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(name='재생')
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else self.nextPlay(ctx))
            await ctx.send(f'현재 재생중: {player.title}')

    @commands.command(name='목록추가')
    async def add_player_list(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            playerlist.append(player)
            await ctx.send(f'목록에 추가됨: {player.title}')

    def nextPlay(self, ctx):
        if not playerlist.__len__() > 0:
            return None

        playerlist.pop(0)

        if ctx.voice_client is None:
            return
        try:
            fut = asyncio.run_coroutine_threadsafe(self.nextPlayCO(ctx), self.bot.loop)
            fut.result()
        except Exception as e:
            print(e)

    async def nextPlayCO(self, ctx):
        async with ctx.typing():
            player = playerlist[0]
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'현재 재생중: {player.title}')

    @commands.command(name='일시정지')
    async def stop(self, ctx):

        ctx.voice_client.pause()

    @commands.command(name='다시재생')
    async def replay(self, ctx):

        ctx.voice_client.resume()

    @commands.command(name='나가기')
    async def leave(self, ctx):
        """Stops and disconnects the bot from voice"""
        playerlist = []
        await ctx.voice_client.disconnect()

    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("음성채널에 접속하고 명령어를 사용해야 됩니다!")
                raise commands.CommandError("명령자가 음성 채널에 연결되어 있지 않습니다.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
