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


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

 




def setup(bot):
    bot.add_cog(Economy(bot))