import os
from discord.ext import commands


class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['reload'])
    @commands.is_owner()
    async def reload_extensions(self, ctx):
        for file in os.listdir('cogs'):
            if file.endswith('.py'):
                name = file[:-3]
                self.bot.reload_extension(f'cogs.{name}')
        await ctx.send('reloaded extensions')

    @commands.command()
    @commands.is_owner()
    async def exit(self, ctx):
        exit()


def setup(bot):
    bot.add_cog(OwnerCog(bot))
