from discord.ext import commands
from core.cog_extension import setting
import os
import asyncio

client = commands.Bot(command_prefix='!')

for filename in os.listdir('./cogs'):  # 讀取所有的cog
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_command_error(ctx, error):  # error處理
    print(f'\n{error}\n')
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f'> 此指令不允許在這頻道使用')
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'> 參數錯誤 {error}')



@setting.is_channel(614856599961600040)
@client.command()
async def load(ctx, extension):  # 載入cog
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'✅**Successfully loaded extension:"{extension}"**')


@setting.is_channel(614856599961600040)
@client.command()
async def unload(ctx, extension):  # 卸載cog
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'✅**Successfully unloaded extension:"{extension}"**')


@setting.is_channel(614856599961600040)
@client.command()
async def reload(ctx, extension):  # 重新載入cog
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'✅**Successfully reloaded extension:"{extension}"**')


client.run(setting.jdict['TOKEN'])
