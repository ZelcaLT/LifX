import datetime
import os 
import aiofiles
import pickle
import nextcord
import aiosqlite
import urllib
import random
from nextcord.ext import ipc, commands
from nextcord.ext.commands.cooldowns import BucketType


class Reports(commands.Cog, name="❌Reports"):
    """In progress"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")




def setup(bot):
    bot.add_cog(Reports(bot))