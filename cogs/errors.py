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


class Errors(commands.Cog, name="Errors"):
    """Used to report bugs in the bot"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if isinstance(error, commands.BadArgument):
                await ctx.reply("You have placed an argument wrong somewhere in the command.")
            elif isinstance(error, commands.BotMissingPermissions):
                await ctx.reply("I am missing permissions for this command.")
            elif isinstance(error, commands.CommandNotFound):
                await ctx.reply("I cannot find that command.")
            elif isinstance(error, commands.CommandOnCooldown):
                await ctx.reply("You are on cooldown. Try again in {:.2f}s".format(error.retry_after))
            elif isinstance(error, commands.MissingPermissions):
                await ctx.reply("You are missing permissions for this command.")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.reply("You are missing a required argument for this command.")
            elif isinstance(error, commands.ChannelNotFound):
                await ctx.reply("That channel does not exist.")
            elif isinstance(error, commands.MemberNotFound):
                await ctx.reply("That member does not exist.")
            elif isinstance(error, commands.MissingRole):
                await ctx.reply("You are missing a role for this command.")
        except:
            if isinstance(error, commands.CommandError):
                em = nextcord.Embed(
                    title="Error ;-;",
                    description="An error occurred while executing this command. The developers have been notified of the error.",
                    color=nextcord.Colour.red()
                )
                em.add_field(name="Error details:", value=error)
                await ctx.reply(embed=em)




def setup(bot):
    bot.add_cog(Errors(bot))
