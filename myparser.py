import discord
import re

def replace_custom_emoji(text:str):
    pattern = r'<:'
    text = re.sub(pattern, '[', text)
    pattern = r':[0-9]+>'
    return re.sub(pattern, ']', text)

def replace_mentisons(text:str, mentions:list[discord.Member]):
    pattern = r'<@&[0-9]+>'
    text = re.sub(pattern, ' ロール ', text)
    for i in mentions:
        pattern = rf'<@!{i.id}>'
        text = re.sub(pattern, i.name if i.nick == "None" else i.name, text)
    return text

def replace_url(text:str):
    pattern = r"https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+"
    text = re.sub(pattern, 'URL', text)
    return text

def parse(message:discord.Message):
    text = message.content.encode('shift-jis', errors='replace').decode('shift-jis')
    text = replace_custom_emoji(text)
    text = replace_mentisons(text, message.mentions)
    text = replace_url(text)
    text = f"{message.author.name if message.author.nick is None else message.author.nick}  {text}"
    print(text)
    return text