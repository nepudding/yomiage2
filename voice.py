import asyncio
from collections import deque
import discord

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

class MyGuild():
    def __init__(self, guild:discord.Guild):
        self.guild = guild
        self.textCh:discord.TextChannel = None
        self.voiceCh:discord.VoiceChannel = None
        self.vClient:discord.VoiceClient = None
        self.vQueue = deque()
        self.mQueue:deque[Pafy] = deque()
        self.varif = {}

    async def send(self,text:str, embed=None):
        await self.textCh.send(content=text, embed=embed)

    @classmethod
    async def connect(cls, textCh:discord.TextChannel, voiceCh:discord.VoiceChannel):
        try:
            ret = cls(textCh.guild)
            ret.textCh = textCh
            ret.voiceCh = voiceCh
            ret.vClient = await ret.voiceCh.connect()
            return ret
        except:
            await textCh.send(content="エラーが発生しました。もう一度コマンドを確かめてください")
            return None

    async def disconnect(self):
        await self.vClient.disconnect()
        self.voiceCh = None
        self.voiceCh = None
        self.vClient = None

    async def playQueue(self, loop):
        if self.vClient is None:
            return
        if self.vClient.is_playing():
            return
        def my_after(error):
            coro = self.playQueue(loop)
            fut = asyncio.run_coroutine_threadsafe(coro, loop)
            fut.result()
        if (len(self.mQueue) > 0):
            await self.playPafy(self.mQueue.popleft(), after = my_after)
        elif(len(self.vQueue) > 0):
            self.playVoice(self.vQueue.popleft(), after = my_after)

    # 読み上げ音声を再生
    def playVoice(self, filePath, after=None):
        self.vClient.play(discord.FFmpegPCMAudio(filePath), after=after)

    async def playPafy(self, music, after=None):
        audio = music.getbestaudio()
        self.vClient.play(discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS), after=after)
        embed=discord.Embed(title="NOW PLAYING!")
        embed.set_thumbnail(url=music.thumb)
        embed.add_field(name="title", value=music.title, inline=True)
        embed.add_field(name="url", value=f"https://www.youtube.com/watch?v={music.videoid}", inline=True)
        embed.add_field(name="play time", value=music.duration, inline=True)
        await self.textCh.send(embed=embed)

class GuildManager():
    def __init__(self):
        self.guilds:dict[MyGuild] = {}

    async def connect(self, textCh, voiceCh):
        guild = await MyGuild.connect(textCh, voiceCh)
        if guild:
            self.guilds[textCh.guild.id] = guild

    async def disconnect(self, guild):
        myguild = self.get_guild(guild)
        if myguild:
            try:
                await myguild.vClient.disconnect()
            finally:
                self.guilds.pop(guild.id)

    async def is_connected(self, guild):
        tmp = self.get_guild(guild)
        if tmp:
            if tmp.vClient.is_connected():
                return True
            else:
                await self.disconnect(guild)
        return False

    def get_guild(self, guild:discord.guild):
        if guild.id in self.guilds:
            return self.guilds[guild.id]
        else:
            return False

    async def addVoice(self, filePath, guild):
        if not await self.is_connected(guild):
            return None
        self.guilds[guild.id].vQueue.append(filePath)

    async def addMusic(self, music, guild):
        if not await self.is_connected(guild):
            return None
        self.guilds[guild.id].mQueue.append(music)
    
    def addVarif(self, message, guild, music):
        self.guilds[guild.id].varif[message.id] = music
    
    async def clickVarif(self, message, emoji):
        g = message.channel.guild
        if not message.id in self.guilds[g.id].varif:
            return False
        if emoji == "✅":
            await self.addMusic(self.guilds[g.id].varif.pop(message.id), g)
            return True
        if emoji == "🚫":
            self.guilds[g.id].varif.pop(message.id)
            return True


    def skip(self, guild:discord.Guild):
        guild = self.get_guild(guild)
        if guild:
            guild.vClient.stop()

    async def send(self, guild, text):
        myguild = self.guilds[guild.id]
        if myguild:
            await myguild.send(text)

    async def play(self, guild, loop):
        guild = self.get_guild(guild)
        if guild:
            await guild.playQueue(loop)