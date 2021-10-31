from datetime import datetime
import discord
import os
from akari import akari
from voice import GuildManager
import myparser
import yt

client = discord.Client()
vRoid = akari()
gManager = GuildManager()

@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)

@client.event
async def on_message(message:discord.Message):
    if message.author.bot:
        return

    # 音楽関係
    if message.content.startswith("!"):
        # 切断
        if message.content.startswith("!l") or message.content.startswith("!leave"):
            await gManager.disconnect(message.channel.guild)
            return
        # 未接続
        if message.author.voice is None:
            await message.channel.send("ボイスチャンネルに接続してから呼んでね")
            return
        # 接続
        elif message.channel.guild.voice_client is None:
            await gManager.connect(message.channel, message.author.voice.channel)
        # 音楽
        if message.content.startswith("!p") or message.content.startswith("!play"):
            keyword = message.content[len(message.content.split()[0])+1:]
            # 曲表示
            embed = discord.Embed(title="Choose music")
            music = await yt.searchMovies(client.loop, keyword)
            embed=discord.Embed(title="Is this the video?", description="If this ok, please click the ✅.\nDifferent, click the 🚫.")
            embed.set_thumbnail(url=music.thumb)
            embed.add_field(name="title", value=f"[{music.title}](https://www.youtube.com/watch?v={music.videoid})", inline=True)
            embed.add_field(name="duration", value=music.duration, inline=True)
            varif = await gManager.guilds[message.channel.guild.id].textCh.send(embed=embed)
            await varif.add_reaction("✅")
            await varif.add_reaction("🚫")
            gManager.addVarif(varif, message.channel.guild, music)

            return

        # スキップ
        if message.content.startswith("!s") or message.content.startswith("!skip"):
            gManager.skip(message.channel.guild)

        return
    
    # 読み上げ
    if await gManager.is_connected(message.channel.guild):
        text = myparser.parse(message)
        print(f"READ {datetime.now().strftime('%Y%m%d%H%M%S%f')}, guildName:{message.channel.guild.name}, text:{text}")
        filename = f"voice/message-{message.id}.wav"
        res = vRoid.textToWav(text, filename)
        await gManager.addVoice(res, message.channel.guild)
        await gManager.play(message.channel.guild, client.loop)

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if not await gManager.is_connected(reaction.message.guild):
        return
    if await gManager.clickVarif(reaction.message, reaction.emoji):
        await reaction.message.delete()
        await gManager.play(reaction.message.channel.guild, client.loop)

if __name__ == "__main__":
    token = os.environ.get("YOMIAGE_TOKEN")
    client.run(token)