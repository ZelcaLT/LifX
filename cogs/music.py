import re, math, os

import nextcord
from nextcord.ext import commands




class Music(commands.Cog, name="🎵Music"):
    """Play music with the bot."""
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")
def setup(bot):
    bot.add_cog(Music(bot))