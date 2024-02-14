import random
import json
import pickle
import numpy as np
import os
import pyttsx3
import subprocess
import time
import discord
#import nacl
from discord.ext.commands import Bot
from discord.ext import commands
from googletrans import Translator
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings("ignore")
import nltk
from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')
#nltk.download('omw-1.4')
import tensorflow
tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)
tensorflow.autograph.set_verbosity(0)
from discord.ext.commands import Bot
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
# client = discord.Client()
from discord.ext import commands
import youtube_dl
#bot = Bot("!")
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
edward = pyttsx3.init()
edward.setProperty('rate', 160)

translator = Translator()

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chat_model.h5')

intent = discord.Intents.all()
intent.members = True
bot = commands.Bot(command_prefix = "!", intents = intent)


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    #THIS LINE BELOW
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result    

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

clearConsole()

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


@bot.event
async def on_message(message: discord.Message):
    # print("Message is working")\
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    if(len(user_message) == 0):
        return
    first_letter = user_message[0]
    if first_letter == "!":
        return
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')
    ctx = await bot.get_context(message)

    if message.author == bot.user:
        return
    # if message.channel.name == 'you-thought-counting-was-hard':
        user_m = user_message   
        print(user_m)
        try: 
            user_m = int(user_m)
            print(type(user_m))
        except: 
            return
        print(type(user_m))
        if type(user_m) == int:
            await message.channel.send(user_m+1)
            return
    if message.channel.name == 'edward':
        if user_message.lower() == 'hello edward':
            await message.channel.send(f'Hello {username}!')
            return
    if message.channel.name == 'edward':
        if user_message == '😡':
            await message.channel.send(f'Angry {username}!')
            return

    #if message.channel.name == 'edward':
        #if user_message.lower() == 'ping random':
            #Channel = message.channel
            #member = random.choice(ctx.guild.members)
            #await ctx.send(member.mention)
            #return
        
    if message.channel.name == 'edward':
        messages = user_message.lower()
        trans = translator.translate(messages, dest="en")
        messages = trans.text
        ints = predict_class(messages)
        res = get_response(ints, intents)
        if res == "you":
            await message.channel.send(f'{username} is the worst member')
            return
        # translation = translator.translate(res, src="en", dest="ko")
        await message.channel.send(res)
        return


# os.system('cls' if os.name == 'nt' else 'clear')
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    #message = message.content
    #ints = predict_class(message)
    #res = get_response(ints, intents)
    #await message.channel.send(res)

bot.run(TOKEN)

#while True:
    #message = input("")
    #ints = predict_class(message)
    #res = get_response(ints, intents)
    #print(f"Edward says {res}")






















