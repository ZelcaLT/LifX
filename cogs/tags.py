import datetime
import os 
import aiofiles
import pickle
import nextcord
import aiosqlite as aio
import urllib
import random
from nextcord.ext import ipc, commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext.commands.cooldowns import BucketType
from nextcord.mentions import A


class Program(commands.Cog, name="💻Python Tags"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")
        
    testServer = 921758771158605834

    @commands.group(name="tag", description="group", invoke_without_command=False)
    async def tag_group(self, ctx):
        pass

    @tag_group.command(name="make")
    async def make(self, ctx, tag_name, tag_desc):
        db_name = "data/tags.db"
        db = await aio.connect(db_name)
        cursor = await db.cursor()
        await cursor.execute("CREATE TABLE IF NOT EXISTS tags (tag_name STR, tag_desc STR, PRIMARY KEY (tag_name, tag_desc))")
        await db.commit()

        await cursor.execute("SELECT * FROM tags WHERE tag_name", (tag_name))
        data = await cursor.fetchone()
        await ctx.send(data[2])





def setup(bot):
    bot.add_cog(Program(bot))