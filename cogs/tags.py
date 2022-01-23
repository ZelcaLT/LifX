import datetime
import os 
import aiofiles
import pickle
import nextcord
import sqlite3 as sq3
import aiosqlite
import urllib
import random
from nextcord.ext import ipc, commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext.commands.cooldowns import BucketType
from nextcord.mentions import A

def createTag(name, description):
    db = sq3.connect('data/tags.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM tag WHERE name = {name}")
    result = cursor.fetchone()

    if result:
        return
    if not result:
        sql = "INSERT INTO tag(name, description) VALUES(?, ?)"
        val = (name, description)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


class Program(commands.Cog, name="💻Python Tags"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")
        
    testServer = 921758771158605834

    @commands.group(name="tag", description="Use a 'tag' for help with programming.", invoke_without_command=True)
    async def tag_group(self, ctx):
        pass

    @tag_group.command(name="make", description="Create a new tag.")
    async def make_tag(self, ctx, name, description):
        try:
            createTag(name, description)

        except Exception as e:
            await ctx.reply(e)
        
        
    







def setup(bot):
    bot.add_cog(Program(bot))