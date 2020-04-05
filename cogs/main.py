import discord
from discord.ext import commands
from core.cog_extension import Cog_extension, setting
import random
from datetime import datetime


class Main(Cog_extension):

    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is ready')
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name='祝福「金榜題名」🧙‍♂️'))

    @commands.Cog.listener()
    async def on_message(self,message):
        random.seed(datetime.now())
        print(f'{setting.tw_tz().strftime("%m/%d-%H:%M")}-{message.channel}-{message.author.name}:{message.content}')
        content = message.content
        if message.author == self.client.user:
            return
        elif content in setting.jdict['key_word']:
            await message.channel.send(setting.jdict['key_word'][content])
        elif content in setting.jdict['pic_key_word']:
            embed = discord.Embed(title="", color=0x009AFF)
            embed.set_image(url=f'{setting.jdict["pic_key_word"][content]}')
            await message.channel.send(embed=embed)
        elif content.endswith("的機率"):
            if content == '你的機率':
                await message.channel.send('Is this a joke?:thinking: ')
                return

            probability = random.randint(0, 100)
            await message.channel.send(f'{probability}% :thinking: ')
            if probability == 100:
                await message.channel.send('騙人的吧...')
            elif probability == 0:
                await  message.channel.send('ㄆ')


    @commands.command()
    async def sayhi(self, ctx):
        await ctx.send('hi')


def setup(client):
    print('----\nmain載入成功')
    client.add_cog(Main(client))