import json
import random
import discord
from discord.ext import commands


class PCP(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='buildpc')
    async def getRecommendedBuilds(self, ctx, price):
        price = int(price)
        deviation = int(price * .07)
        guide_viable_builds = []
        completed_viable_builds = []

        build_guides = readJson('cogs/json_guides/buildguide.json')
        for guide in build_guides:
            if price - deviation <= guide['price'] <= price + deviation:
                guide_viable_builds.append(guide)

        completed_guides = readJson('cogs/json_guides/completedguide.json')
        for guide in completed_guides:
            if price - deviation <= guide['price'] <= price + deviation:
                completed_viable_builds.append(guide)
        
        if not guide_viable_builds and not completed_viable_builds:
            message = f'> Could not a find build around ${str(price)}'
            await ctx.send(content=message)
            return 
        else:
            message = f'> Here are some builds around ${str(price)}\n'

        if guide_viable_builds:
            message += '\n> **From the build guides**\n'
            if len(guide_viable_builds) > 2:
                choices = random.choices(guide_viable_builds, k=2)
                for choice in choices:
                    message += addMessage(choice)
            else:
                for choice in guide_viable_builds:
                    message += addMessage(choice)
        
        if completed_viable_builds:
            message += '\n> **From completed builds**\n'
            if len(completed_viable_builds) > 3:
                choices = random.choices(completed_viable_builds, k=3)
                for choice in choices:
                    message += addMessage(choice)
            else:
                for choice in completed_viable_builds:
                    message += addMessage(choice)

        await ctx.send(content=message[:-3])


def addMessage(choice):
    message = f'> __{choice["title"]}__\n'
    message += f'> {choice["cpu"]}      {choice["gpu"]}\n'
    message += f'> ${str(choice["price"])}\n'
    message += f'> <{choice["link"]}>\n'
    message += '> \n'
    return message 


def readJson(path: str) -> str:
    with open(path) as f:
        return json.load(f)


def setup(bot):
    bot.add_cog(PCP(bot))