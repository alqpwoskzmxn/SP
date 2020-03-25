import discord
from konlpy.tag import Okt
import nltk

okt = Okt()

class MyClient(discord.Client):
    messagelist = []
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == '>topic':
            await message.channel.send('The Topic is ' + self.messagelist[0])
        elif message.content == '>train':
            await message.channel.send('Training')
            text = nltk.Text(self.messagelist, name='NMSC')
            print(text.vocab().most_common(10))
        else:
            self.messagelist = self.messagelist + okt.pos(message.content, norm=True, stem=True, join=True)
            print(self.messagelist)

    async def on_typing(self, channel, user, when):
        print(user.name + '(' + str(user.id) + ') is typing')

client = MyClient()
client.run(open('token', 'r').read())
