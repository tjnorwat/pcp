import os
import json
import discord
import buildguide
import completedguide
from discord.ext import commands


def get_prefix(bot, message):
    prefix = '?'
    return commands.when_mentioned_or(*prefix)(bot, message)

bot = commands.Bot(command_prefix=get_prefix)

@bot.event
async def on_ready():
    print(f'Logging in as {bot.user.name}')
    await bot.change_presence()


if __name__ == '__main__':
    
    for file in os.listdir('cogs'):
        if file.endswith('.py'):
            name = file[:-3]
            bot.load_extension(f'cogs.{name}')

    with open('config.json') as f:
        config = json.load(f)

    bot.run(config['token'], bot=True)