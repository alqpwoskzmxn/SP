import discord
from konlpy.tag import Okt
import nltk
from gensim.models import word2vec

okt = Okt()
model = ''


class MyClient(discord.Client):
    messagelist = []
    model = ''
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == '>topic':
            a = ''
        elif message.content == '>train':
            await message.channel.send('Training')
            self.model = word2vec.Word2Vec(self.messagelist, size=100, window=3, iter=100)
            await message.channel.send('Training end')
        elif message.content == '>reset':
            self.model = ''
            self.messagelist = []

        else:
            self.messagelist = self.messagelist + \
                okt.pos(message.content, norm=True, stem=True, join=True)
            print(self.messagelist)

    async def on_typing(self, channel, user, when):
        print(user.name + '(' + str(user.id) + ') is typing')


client = MyClient()
client.run(open('token', 'r').read())
