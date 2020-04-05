import discord
from discord.ext import commands
from core.cog_extension import Cog_extension, setting
import json
import urllib.request as loadWeb
import asyncio


class ServerClock(Cog_extension):

    # ---------------每分鐘跑一次指定的Function---------------
    async def loop_events(self):
        while True:
            try:
                await asyncio.sleep(60 - int(setting.tw_tz().strftime('%S')))
                await self.client.get_channel(647767636909883392).edit(name=setting.tw_tz().strftime('%A %H{}%M').format('：'))
                await ServerClock.weather(self)
            except Exception as e:
                print(e)

    # ---------------連接中央氣象局天氣api並修改頻道名稱---------------
    async def weather(self):
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-00' \
              '1?Authorization=CWB-B20612A4-C042-45B3-AEE7-57D8D8CDF93B&format' \
              '=JSON&locationName=%E9%AB%98%E9%9B%84%E5%B8%82&elementName=Wx,CI,MinT,MaxT&sort=time'
        request = loadWeb.Request(url)
        with loadWeb.urlopen(request) as response:
            data = response.read().decode('utf-8')
        jdata = json.loads(data)
        ks_wea = jdata["records"]["location"][0]["weatherElement"]  # 高雄天氣資訊
        startTime = ks_wea[0]["time"][1]["startTime"].strip('00:00') + '點'  # 起始時間
        endTime = ks_wea[0]["time"][1]["endTime"].strip('00:00') + '點'  # 最後時間
        weaContent = ks_wea[0]["time"][1]["parameter"]["parameterName"]  # 天氣簡述
        maxT = ks_wea[3]["time"][1]["parameter"]["parameterName"]  # 最高溫度
        minT = ks_wea[1]["time"][1]["parameter"]["parameterName"]  # 最低溫度
        feeling = ks_wea[2]["time"][1]["parameter"]["parameterName"]  # 體感

        time_channel = self.client.get_channel(660673766019301376)
        weaCont_channel = self.client.get_channel(660673909548515328)
        temp_channel = self.client.get_channel(660674179510829057)
        feeling_channel = self.client.get_channel(660674271042994227)

        await time_channel.edit(name=f'{startTime}')
        await weaCont_channel.edit(name=f'{weaContent}')
        await temp_channel.edit(name=f'{minT}℃到{maxT}℃')
        await feeling_channel.edit(name=f'{feeling}')

    # ---------------手動重啟伺服器時鐘---------------
    @setting.is_channel(631816736563527680,614856599961600040)
    @commands.command(pass_context=True)
    async def server_clock(self, ctx):
        print('{}'.format(setting.tw_tz().strftime('%S')))
        channel = self.client.get_channel(647767636909883392)
        while True:
            await asyncio.sleep(60 - int(setting.tw_tz().strftime('%S')))
            await channel.edit(name=setting.tw_tz().strftime('%A %H{}%M').format('：'))

    # ---------------bot啟動時要跑的Function---------------
    @commands.Cog.listener()
    async def on_ready(self):
        print('server_clock is ready!')
        await ServerClock.loop_events(self)


def setup(client):
    print('----\nserver_clock載入成功')
    client.add_cog(ServerClock(client))