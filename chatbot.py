import random
import json
import pickle
import numpy as np
import os
import pyttsx3
import subprocess
import time
import discord
from googletrans import Translator
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings("ignore")
import nltk
from nltk.stem import WordNetLemmatizer
# nltk.download('wordnet')
# nltk.download('omw-1.4')
import tensorflow
tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)
tensorflow.autograph.set_verbosity(0)

from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
TOKEN = "MTAwNDE0NzE1MzAyNDg2MDI5MQ.GVOqtt.SM_DQwpT7vru_2YtnDz5OT3VeoSVzb6Y84p_UI"
client = discord.Client()

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

edward = pyttsx3.init()
edward.setProperty('rate', 160)

translator = Translator()

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chat_model.h5')

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

# os.system('cls' if os.name == 'nt' else 'clear')
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print("Message is working")
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')
    

    if message.author == client.user:
        return
    if message.channel.name == 'edward':
        if user_message.lower() == 'hello edward':
            await message.channel.send(f'Hello {username}!')
            return
    if message.channel.name == 'edward':
        if user_message == '😡':
            await message.channel.send(f'Angry {username}!')
            return
    if message.channel.name == 'edward':
        if user_message == '🔫':
            await message.channel.send(f' {username} 🔫')
            return
    

    if message.channel.name == 'edward':
        messages = user_message.lower()
        trans = translator.translate(messages, dest="en")
        messages = trans.text
        ints = predict_class(messages)
        if len(ints) == 0:
            #translation = translator.translate("I don't understand you", src="en", dest="ko")
            await message.channel.send("I don't understand you")
            return
        res = get_response(ints, intents)
        if res == "":
            #translation = translator.translate("I don't understand you", src="en", dest="ko")
            await message.channel.send("I don't understand you")
            return
        if res == "you":
            await message.channel.send(f'{username} is the worst member')
            return
        # translation = translator.translate(res, src="en", dest="ko")
        await message.channel.send(res)
        return







    #message = message.content
    #ints = predict_class(message)
    #res = get_response(ints, intents)
    #await message.channel.send(res)

client.run(TOKEN)

#while True:
    #message = input("")
    #ints = predict_class(message)
    #res = get_response(ints, intents)
    #print(f"Edward says {res}")





















