import discord
from discord.ext import commands
from core.cog_extension import Cog_extension, setting
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request as loadWeb
import urllib.parse


class ImfoCrawler(Cog_extension):

    # ---------------颱風搜尋指令---------------
    @setting.is_channel(595987187481182220, 614856599961600040)
    @commands.command()
    async def typhoon(self, ctx):

        try:
            async with ctx.typing():
                url = 'https://www.cwb.gov.tw/V8/C/P/Typhoon/TY_NEWS.html'
                options = Options()
                options.headless = True
                driver = webdriver.Chrome(options=options)
                driver.get(url)
                html = driver.page_source
                driver.quit()
                soup = BeautifulSoup(html, 'html.parser')

                overall = soup.find('span', id='TY_COUNT').text
                typhoon = soup.find('a', class_='accordion-toggle').text
                image = 'https://www.cwb.gov.tw' + soup.find('img', id='slideImage-1')['src']

                embed = discord.Embed(title=f'{overall}', description=f'{typhoon}')
                embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            embed = discord.Embed(title=f'目前沒有颱風(^_^)/',
                                  description=f'不信你自己去看 \n'f'[交通部中央氣象局傳送門]'
                                  f'(https://www.cwb.gov.tw/V8/C/P/Typhoon/TY_NEWS.html)\n\n如果有錯請叫'
                                  f'{self.client.get_user(254808247884709892).name}  :P')
            await ctx.send(embed=embed)

    # ---------------Google News搜尋指令---------------
    @setting.is_channel(595987187481182220, 614856599961600040)
    @commands.command()
    async def news(self, ctx, *, news_search):
        async with ctx.typing():
            news_url = f'https://news.google.com/search?q={urllib.parse.quote(news_search)}&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
            request = loadWeb.Request(news_url)
            with loadWeb.urlopen(request) as response:
                data = response.read().decode('utf-8')
            soup = BeautifulSoup(data, 'html.parser')
        try:
            title = soup.find_all('a', class_='DY5T1d')
            media = soup.find_all('a', class_='wEwyrc AVN2gc uQIVzc Sksgp')
            time_ago = soup.find_all('time', class_='WW6dff uQIVzc Sksgp')
            test = ''
            embed = discord.Embed(title=f'{news_search}搜尋結果')

            for i in range(10):
                print(f'\t{i+1}.{title[i].text}----{media[i].text} {time_ago[i].text}')
                test = test + f'{title[i].text}----{media[i].text}\n' + 'https://news.google.com/' + title[i][
                    'href'] + '\n'
                embed.add_field(name=f'{i + 1}.  {time_ago[i].text}',
                                value=f'[{title[i].text}----{media[i].text}]({"https://news.google.com/" + title[i]["href"]})', inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f'!news指令錯誤:{e}')
            await ctx.send('窩不到新聞 <:emoji_17:624093478057541654>')




def setup(client):
    print('----\nimfo_crawler載入成功')
    client.add_cog(ImfoCrawler(client))