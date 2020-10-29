import discord
from konlpy.tag import Okt
from hanspell import spell_checker

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib

import re

okt = Okt()

model = joblib.load('model.pkl')
tfidfvect = joblib.load('tfidf.pkl')


class MyClient(discord.Client):
    messagelist = []
    topic = []

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == '>topic':
            await message.channel.send('The topic of this channel is ' + max(self.topic, key=self.topic.count))

        elif message.content == '>last_topic':
            await message.channel.send('The topic of last chat was ' + self.topic[-1])

        elif message.content == '>reset':
            self.topic = []
            self.messagelist = []

        else:
            new_message = re.sub("[^가-힣 ]", "", message.content)
            new_message = spell_checker.check(new_message)
            new_message = new_message.checked
            new_message = [' '.join(okt.morphs(new_message, stem=True))]

            message_tfidf = tfidfvect.transform(new_message).toarray().tolist()

            self.topic.append(model.predict(message_tfidf)[0])
            self.messagelist.append(new_message)
            print(self.messagelist)

    async def on_typing(self, channel, user, when):
        print(user.name + '(' + str(user.id) + ') is typing')


client = MyClient()
client.run(open('token', 'r').read())
