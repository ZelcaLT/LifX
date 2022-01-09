import datetime
import urllib
import os 
import aiofiles
import nextcord
import aiosqlite
import urllib
import json
import asyncio
import datetime
from nextcord import channel
from nextcord.components import Button
from nextcord.ext import ipc, commands
from nextcord.ext.commands.cooldowns import BucketType
from nextcord.ext.commands.errors import MissingRequiredArgument
from nextcord.types.components import ButtonStyle

class Fun(commands.Cog, name="😂Fun"):

    def __init__(self, bot):
        self.bot = bot

        
    """Cogs for memes and jokes, or practical like `invite`"""
   



    @commands.command(name="meme", description="A meme command that generates a meme from Reddit.")
    async def meme(self, ctx):
        memeApi = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme")

        memeData = json.load(memeApi)

        memeUrl = memeData["url"]
        memeName = memeData["title"]
        memePoster = memeData["author"]
        memeSub = memeData["subreddit"]
        memeLink = memeData["postLink"]

        embed = nextcord.Embed(title=memeName)
        embed.set_image(url=memeUrl)
        embed.set_footer(text=f"Made by: {memePoster} | Subreddit: {memeSub} | Post: {memeLink}")
        await ctx.send("heres ya meme u granny")
        await ctx.send(embed=embed)

    @commands.command(name="say", description="Say something as the bot.")
    async def say(self, ctx, message):
        await ctx.message.delete()
        await ctx.send(message + "\n\n\- {}".format(ctx.author.display_name))








def setup(bot):
    bot.add_cog(Fun(bot))