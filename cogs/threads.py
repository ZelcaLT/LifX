import datetime
import os 
import aiofiles
import asyncio
import nextcord
import aiosqlite
import urllib
import random
import main
from nextcord.ext import ipc, commands
from nextcord.ext.commands.cooldowns import BucketType


class CodeHelp(commands.Cog, name="🖱Programming Help"):
    """Programming help in **The Coders**"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")

    @commands.command()
    @commands.cooldown(1, 360, BucketType.member)
    async def pghp(self, ctx, language, *, problem):
        if ctx.channel.id == 927366458323910676:
            await ctx.message.delete()
            view = main.CodeButtons()
            print(language, problem)
            thread = await ctx.channel.create_thread(name=f"{ctx.author.display_name}_{language}", type=nextcord.ChannelType.public_thread)
            await thread.send(f"Author: `{ctx.author}`Problem: `{problem}`\nLanguage: `{language}`", view=view)
            await view.wait()
            if view.value:
                if ctx.author:
                    await thread.delete()
                    return await ctx.author.send(f"Your thread in `{ctx.guild}` has been deleted.\nName: `{thread.name}`\nLanguage: `{language}`\nProblem: `{problem}`")
        else:
            return await ctx.reply("You cannot make a help thread in this channel!")





def setup(bot):
    bot.add_cog(CodeHelp(bot))