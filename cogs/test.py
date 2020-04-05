import discord
from discord.ext import commands
from core.cog_extension import Cog_extension, setting


class Test(Cog_extension):
    @commands.command()
    async def number(self,ctx,month:int):
        await ctx.send(month)

    @commands.command()
    async def pyramid(self, ctx, floor: int):
        if floor > 40:
            return
        a = 1
        output = '```\n'
        for i in range(floor):
            for j in range(floor - i):
                output=output+' '
            for k in range(i + a):
                output=output+'*'
            a = a + 1
            output=output+'\n'
        output=output+'```'
        await ctx.send(output)

    @commands.command()
    async def birthday(self, ctx, *, user_id):
        embed = discord.Embed(title=f'祝{user_id}生日快樂',color=0xFF0080)
        embed.set_image(url='https://i.ytimg.com/vi/nZEIpHSILzw/hqdefault.jpg')
        await ctx.send(embed=embed)




def setup(client):
    print('----\ntest載入成功')
    client.add_cog(Test(client))
