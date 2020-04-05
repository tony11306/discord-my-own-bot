import discord
from discord.ext import commands
import json
from core.cog_extension import Cog_extension, setting
import asyncio
from datetime import datetime


class Remind(Cog_extension):

    # ---------------新增提醒指令---------------
    @setting.is_channel(651753845680111616, 614856599961600040)
    @commands.command()
    async def remind(self, ctx, task, month: int, day: int, hour: int, min: int):
        if month < 1 or month > 12:
            await ctx.send('> 月份錯誤，須介在1~12之間')
            return
        elif day < 1 or day > 31:
            await ctx.send('> 日期錯誤，須介在1~31之間')
            return
        elif hour < 0 or hour > 24:
            await ctx.send('> 小時錯誤，須介在0~24之間')
            return
        elif min < 0 or min >59:
            await ctx.send('> 分鐘錯誤，須介在0~59之間')
            return
        remind_time = datetime(int(setting.tw_tz().strftime("%Y")), month, day, hour, min, 0, 0).replace(tzinfo=None)
        current_time = setting.tw_tz().replace(tzinfo=None)
        if remind_time < current_time:
            await ctx.send('> 不能設置以前的時間')
            return
        user_id = ctx.author.id
        name = ctx.author.name
        with open('remind.json', 'r', encoding='utf8') as jdata:
            jremind = json.load(jdata)
        if str(user_id) in jremind:

            jremind[str(user_id)]['task'][task] = f"{month}/{day}-{hour}:{min}"
            with open('remind.json', 'w', encoding='utf8') as jdata:
                json.dump(jremind, jdata, ensure_ascii=False)
        else:
            jremind[user_id] = {}
            jremind[user_id]['name'] = name
            jremind[user_id]['task'] = {}
            jremind[user_id]['task'][task] = f"{month}/{day}-{hour}:{min}"
            print('test')
            with open('remind.json', 'w', encoding='utf8') as jdata:
                json.dump(jremind, jdata, ensure_ascii=False)
        await ctx.send(f'OK! {ctx.author.name},  已將「{task}」新增於列表中，會在{month}/{day}-{hour}:{min}通知!')

    # ---------------顯示使用者的提醒清單指令---------------
    @setting.is_channel(651753845680111616, 614856599961600040)
    @commands.command()
    async def remindlist(self, ctx):
        with open('remind.json', 'r', encoding='utf8') as jdata:
            jremind = json.load(jdata)
        if jremind.get(str(ctx.author.id)) is None:
            await ctx.send('你沒在我們名冊上喔 去新增個提醒我才能取得你的資料')
            return
        user_tasks = jremind[str(ctx.author.id)]['task']
        string = f'User:{ctx.author.name}\n\n'
        for key, value in user_tasks.items():
            string = string + f'事件:{key} 時間:{value}\n'
            print(f'User:{ctx.author.name}\n\n事件:{key} 時間:{value}')
        await ctx.send(f'```{string}```')

    # ---------------移除使用者指定事件指令---------------
    @setting.is_channel(651753845680111616, 614856599961600040)
    @commands.command()
    async def remindrmv(self, ctx, task):
        with open('remind.json', 'r', encoding='utf8') as jdata:
            jremind = json.load(jdata)
        if jremind.get(str(ctx.author.id)) is None:
            await ctx.send('你沒在我們名冊上喔 去新增個提醒我才能取得你的資料')
            return
        with open('remind.json', 'w', encoding='utf8') as jdata:
            for key, value in jremind[str(ctx.author.id)]['task'].items():
                if task == key:
                    del jremind[str(ctx.author.id)]['task'][task]
                    json.dump(jremind, jdata, ensure_ascii=False)
                    await ctx.send(f'**事件「{task}」已移除!**')
                    return
            await ctx.send(f'你確定你有「{task}」這設定?')
            json.dump(setting.jremind, jdata, ensure_ascii=False)

    # ---------------每分鐘跑一次指定的Function---------------
    async def loop_events(self):
        while True:
            try:
                await asyncio.sleep(60 - int(setting.tw_tz().strftime('%S')))
                await Remind.task_update(self)
            except Exception as e:
                print(e)

    # ---------------偵測是否為提醒的時刻---------------
    async def task_update(self):
        with open('remind.json', 'r', encoding='utf8') as jdata:
            jremind = json.load(jdata)
        for key, value in jremind.copy().items():
                for key2, value2 in value['task'].copy().items():
                    if f'{int(setting.tw_tz().strftime("%m"))}/{int(setting.tw_tz().strftime("%d"))}-{int(setting.tw_tz().strftime("%H"))}:{int(setting.tw_tz().strftime("%M"))}' == value2:
                        del value['task'][key2]
                        with open('remind.json', 'w', encoding='utf8') as jdata:
                            json.dump(jremind, jdata, ensure_ascii=False)
                        remind_embed = discord.Embed(title=f'⏰提醒!', description=f'{self.client.get_user(int(key)).mention}')
                        remind_embed.add_field(name='Task:', value=f'{key2}')
                        message = await self.client.get_channel(651753845680111616).send(self.client.get_user(int(key)).mention)
                        await discord.Message.edit(message, embed=remind_embed)
                        print(f'{self.client.get_user(int(key)).name}\n{key2}')

    # ---------------bot啟動時要跑的Function---------------
    @commands.Cog.listener()
    async def on_ready(self):
        await Remind.loop_events(self)


def setup(client):
    print('----\nremind載入成功')
    client.add_cog(Remind(client))