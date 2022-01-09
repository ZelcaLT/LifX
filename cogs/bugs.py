import datetime
import os 
import aiofiles
import pickle
import nextcord
import aiosqlite
import urllib
import random
from nextcord.ext import ipc, commands
import config
from nextcord.ext.commands.cooldowns import BucketType


class Bugs(commands.Cog, name="🕷Bugs"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")
    
    @commands.command(name="bug", description="Sends a bug report to the developers.", aliases=["br"])
    async def bug(self, ctx, *, reason=None):
        if reason == None:
            await ctx.reply("You need a reason to report a bug!")
            return

        author = ctx.author
        bug_report_channels = self.bot.get_channel(927360499182600252)
        embed = nextcord.Embed(color=nextcord.Colour.random())
        embed.title = ("Bug Reported")
        embed.description = (f"A bug was reported to the developers by {author.mention}.\n\n\n{reason}")
        embed.set_author(name=author.name, icon_url=author.avatar.url)
        await ctx.send(embed=embed)



        await ctx.reply(f"Your bug report has been sent to the developers.\nSee your bug report in my support server. Join by using the command `{config.prefix}invite`")




def setup(bot):
    bot.add_cog(Bugs(bot))