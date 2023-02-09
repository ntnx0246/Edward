import discord
import youtube_dl
import os
import time
#import PyNaCl
from discord.ext import commands
TOKEN = "MTAwNDE0NzE1MzAyNDg2MDI5MQ.GaYaZU.nXyERsn2ABxaRwSk3gbQ-ujtFuZlUx6MMUWj5c"

intent = discord.Intents.all()

bot = commands.Bot(command_prefix = "!", intents = intent)


@bot.command()
async def join(ctx):

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Rec Room')
    await voiceChannel.connect()
    #channel = ctx.author.voice.channel
   # await channel.connect()

@bot.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Music Playing")
        return
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    ydl_opts = {    
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    #for file in os.listdir("./"):
        #if file.endswith(".mp3"):
            #video = VideoFileClip(os.path.join(file.mp4))
            #video.audio.write_audiofile(os.path.join("song.mp3"))
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    print("Working")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    #for i in range(0, 5):
        #if voice.is_playing() == False:
            #voice.play(discord.FFmpegPCMAudio("song.mp3"))
            #while True:
                #time.sleep(5)
                #print(voice.is_playing())
                #if voice.is_playing() == False:
                    #return
    #time.sleep(3)
    #if voice.is_playing() == False:
        #time.sleep(15)
        #voice.play(discord.FFmpegPCMAudio("song.mp3"))
    

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else: 
        await ctx.send("I can't leave")

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else: 
        await ctx.send("I can't pause")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else: 
        await ctx.send("I can't resume")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

#@bot.event
#async def on_message(message):
   #if message.author.id == 641133678055129099:
        #while True:
            #await message.author.send("🔪")
            #time.sleep(0.1)
   #print(message.author.id)
   #return
   #msg = message.content

   #if msg.startswith('Hello!'):
   #await message.author.send("Well hello there!")


@bot.command()
async def cont(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("song.mp3"))



bot.run(TOKEN)  

#@bot.event
#async def on_ready():   
