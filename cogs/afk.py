from nextcord.ext import commands

afk = {}

class afks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(afks(bot))
