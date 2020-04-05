import discord
from discord.ext import commands
from core.cog_extension import Cog_extension, setting
from bs4 import BeautifulSoup
import urllib.request as loadWeb
import random
from datetime import datetime
import asyncio


question_lock = False


class English(Cog_extension):

    # ---------------劍橋英文字典搜尋指令---------------
    @setting.is_channel(614856599961600040, 632149683384352778)
    @commands.command()
    async def search(self, ctx, *, word: str):

        try:
            async with ctx.typing():
                try:
                    part_of_speech = []
                    Youglish_url = f'https://youglish.com/pronounce/{word.split(".search ")[0].replace(" ","%20")}/english?'
                    url = f'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{word.split(".search ")[0].replace(" ", "-")}'
                    request = loadWeb.Request(url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
                    })
                    with loadWeb.urlopen(request) as response:
                        data = response.read().decode('utf-8')
                    soup = BeautifulSoup(data, 'html.parser')
                    examination = soup.find('div', attrs={'class': 'di-title'}).text
                except:
                    part_of_speech = []
                    Youglish_url = f'https://youglish.com/pronounce/{word.split(".search ")[0].replace(" ","%20")}/english?'
                    url = f'https://dictionary.cambridge.org/dictionary/english/{word.split(".search ")[0].replace(" ","-")}'
                    request = loadWeb.Request(url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
                    })
                    with loadWeb.urlopen(request) as response:
                        data = response.read().decode('utf-8')
                    soup = BeautifulSoup(data, 'html.parser')
                print(url)
                for i in soup.find_all('span', attrs={'class': 'pos dpos'}):
                    part_of_speech.append(i.text)
                define = soup.find('div', attrs={'class': 'def ddef_d db'}).text
                print(f'{ctx.author.name}-查找字詞:{word.split(".search ")[0]}')
                print(set(part_of_speech))
                whole_text = soup.find('div', attrs={'class': 'def-body ddef_b'}).text
                print(whole_text)
                if whole_text == ' ':
                    embed = discord.Embed(title=f'{word.split(".search")[0]}搜尋結果',
                                          description=f'可當詞性{str(part_of_speech)}', color=0xff0000)
                    embed.add_field(name='解釋:', value=define, inline=False)
                    embed.add_field(name='劍橋辭典Cambridge Dictionary:', value=f'[{word.split(".search")[0]}更多意思]({url})',
                                    inline=False)
                    embed.add_field(name='Youglish:', value=f'[{word.split(".search")[0]}看看母語者怎麼用]({Youglish_url})',
                                    inline=False)
                    embed.set_footer(text=f'{setting.tw_tz().strftime("%Y")}年{setting.tw_tz().strftime("%m")}月{setting.tw_tz().strftime("%d")}日 {setting.tw_tz().strftime("%A %H:%M")}')
                else:
                    embed = discord.Embed(title=f'{word.split(".search")[0]}搜尋結果',
                                          description=f'可當詞性{str(part_of_speech)}', color=0xff0000)
                    embed.add_field(name='解釋:', value=define, inline=False)
                    embed.add_field(name='範例:', value=whole_text, inline=False)
                    embed.add_field(name='劍橋辭典Cambridge Dictionary:', value=f'[{word.split(".search")[0]}更多意思]({url})',
                                    inline=False)
                    embed.add_field(name='Youglish:', value=f'[{word.split(".search")[0]}看看母語者怎麼用]({Youglish_url})',
                                    inline=False)
                    embed.set_footer(text=f'{setting.tw_tz().strftime("%Y")}年{setting.tw_tz().strftime("%m")}月{setting.tw_tz().strftime("%d")}日 {setting.tw_tz().strftime("%A %H:%M")}')

            await ctx.send(embed=embed)
        except:
            await ctx.send('蝦咪挖哥小 我找不到拉幹')

    # ---------------英文單字抽背指令---------------
    @setting.is_channel(614856599961600040,632149683384352778)
    @commands.command()
    async def question(self, ctx, version=None):
        global question_lock  # 防止多重呼叫後產生bug的防範機制
        if question_lock:
            await ctx.send(f'**{ctx.author.name}請稍等/ question lock status:{question_lock}**')
            return
        question_lock = True
        if version == 'gsat' :
            voc = setting.voc
        elif version == 'toeic':
            voc = setting.toeic_voc
        else:
            await ctx.send('> 使用方法:\n> /question [考題版本], \"gsat\"為學測單字範圍, \"toeic\"為多益單字範圍')
            question_lock = False
            return
        caller = ctx.author
        grade = 0
        answer = ''
        cambridge_url = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/'
        random.seed(datetime.now())

        try:
            for times in range(0, 10):
                AC_index = random.randrange(0, 4)
                question = random.sample(voc, k=7)
                print(AC_index)
                embed = discord.Embed(title='Question', color=0xff0000)
                embed.set_author(name=f'({times + 1}/10) {caller.name}的試煉',
                                 icon_url='https://p7.hiclipart.com/preview/805/133/210/thinking-emoji-sticker-thought-discord-emoji.jpg')
                embed2 = discord.Embed(title=f'which one is 「{str(question[AC_index][1])}」\n解答來囉(可以點擊網址查詢用法)',
                                       color=0x00FF00)
                embed2.set_author(name=f'({times + 1}/10) {caller.name}的試煉',
                                  icon_url='https://p7.hiclipart.com/preview/805/133/210/thinking-emoji-sticker-thought-discord-emoji.jpg')
                embed.add_field(name=f'which one is {str(question[AC_index][1])}', value='只有十秒鐘喔!', inline=False)
                j = 4
                slot = ['(A)', '(B)', '(C)', '(D)']
                detail_explanation = []
                for i in range(0, 4):
                    if i == AC_index:
                        url_statement = question[i][0].replace(' ','%20')
                        detail_explanation.append(
                            f'{str(slot[i])} {str(question[AC_index][0])} : {str(question[AC_index][1])}')
                        embed.add_field(name=slot[i], value=str(question[AC_index][0]), inline=False)
                        embed2.add_field(name=slot[i],
                                         value=f'[{str(question[i][0])}]({cambridge_url + str(url_statement)}) : {str(question[i][1])}', inline=False)
                        continue
                    else:
                        url_statement = question[j][0].replace(' ', '%20')
                        detail_explanation.append(f'{str(slot[i])} {str(question[j][0])} : {str(question[j][1])}')
                        embed.add_field(name=slot[i], value=str(question[j][0]), inline=False)
                        embed2.add_field(name=slot[i],
                                         value=f'[{str(question[j][0])}]({cambridge_url + str(url_statement)}) : {str(question[j][1])}', inline=False)
                    j = j + 1

                print(detail_explanation)
                if times == 0:
                    message = await ctx.send(embed=embed)
                else:
                    await discord.Message.edit(message, embed=embed)

                emoji1 = ['🇦', '🇧', '🇨', '🇩', '▶', '✅', '❌']
                await discord.Message.add_reaction(message, emoji1[0])
                await discord.Message.add_reaction(message, emoji1[1])
                await discord.Message.add_reaction(message, emoji1[2])
                await discord.Message.add_reaction(message, emoji1[3])

                def check(reaction, user):
                    return str(reaction.emoji) in emoji1 and user == caller

                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=10.0, check=check)
                    answer = str(reaction.emoji)
                except asyncio.TimeoutError:
                    embed3 = embed2
                    embed3.add_field(name='喜哩困逆', value='別再睡了啦', inline=False)
                    await discord.Message.edit(message, embed=embed3)
                    await discord.Message.add_reaction(message, '❌')
                    await discord.Message.add_reaction(message, '▶')
                else:
                    if str(reaction.emoji) == emoji1[AC_index]:
                        await discord.Message.add_reaction(message, '✅')
                        await discord.Message.add_reaction(message, '▶')
                        await discord.Message.edit(message, embed=embed2)
                        grade = grade + 10
                    else:
                        await discord.Message.add_reaction(message, '❌')
                        await discord.Message.edit(message, embed=embed2)
                        await discord.Message.add_reaction(message, '▶')
                if times != 9:
                    while True:
                        try:
                            reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)
                        except asyncio.TimeoutError:
                            break
                        else:
                            if str(reaction.emoji) == emoji1[4]:
                                break
                            continue
                for i in emoji1:
                    if i == '✅' or i == '❌' or i == '▶':
                        await discord.Message.remove_reaction(message, emoji=i, member=message.author)
                    elif i == answer:
                        await discord.Message.remove_reaction(message, emoji=i, member=caller)
                    await discord.Message.remove_reaction(message, emoji='▶', member=caller)
            embed2.add_field(name=f'{caller}總得分:', value=f'{grade}分', inline=False)
            await discord.Message.edit(message, embed=embed2)
            question_lock = False
        except:
            question_lock = False
            await ctx.send(f'**錯誤/ question lock status:{question_lock}**')


def setup(client):
    print('----\nenglish載入成功')
    client.add_cog(English(client))