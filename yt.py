from googleapiclient.discovery import build
import pafy
import re
import asyncio
import os
import discord

youtube = build('youtube', 'v3', developerKey=os.environ.get('GCP_API_KEY'))

# キーワードから動画を検索
def searchMovie(keyword):
    if is_yt_url(keyword):
        return pafy.new(keyword)
    part = "id"
    search = youtube.search().list(part=part, q=keyword, order="relevance", type='video', safeSearch="strict")
    res = search.execute()
    for item in res['items']:
        music = pafy.new(f'https://www.youtube.com/watch?v={item["id"]["videoId"]}')
        if music.duration != '00:00:00':
            return music
    if len(ret) <= 0:
        return pafy.new(f'https://www.youtube.com/watch?v=-TPUIkfJIb4')

# キーワードからlist[Pafy]を返す
async def searchMovies(loop, keyword):
    loop = loop or asyncio.get_event_loop()
    ret = await loop.run_in_executor(None, searchMovie, keyword)
    return ret

def is_yt_url(word):
    if word.startswith("http") and 'youtu' in word:
        return True
    else:
        return False