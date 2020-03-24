import discord

class MyClient(discord.Client):
    s = ''
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('>'):
            await message.channel.send('This is Command')
            print('Command Input')
        else:
            self.s += message.content

    async def on_typing(self, channel, user, when):
        print(user.name + '(' + str(user.id) + ') is typing')
        await channel.send('typing')

client = MyClient()
client.run(open('token', 'r').read())

