import datetime
import os 
import aiofiles
import pickle
import youtube_dl
import nextcord
import aiosqlite
import urllib
import random
from nextcord.ext import ipc, commands
from nextcord.ext.commands.cooldowns import BucketType


class Music(commands.Cog, name="🎵Music"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")

    @commands.command(name="join", description="Joins the voice channel you are in.")
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.reply("You are not in a voice channel!")
            return
        vc = ctx.author.voice.channel
        if ctx.voice_client is None:
            await vc.connect()
            await ctx.reply("I have joined the voice channel.")
        else:
            await ctx.voice_client.move_to(vc)

    @commands.command(name="disconnect", description="Leaves the voice channel.", aliases=["dc"])
    async def discconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.reply("I have disconnected from the voice channel.")

    @commands.command(name="play", description="Plays a song in the voice channel.")
    async def play(self, ctx, url):
        ctx.voice_client.stop()
        YDL_OPTIONS = {"format":"bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info["formats"][0]["url"]
            source = await nextcord.FFmpegPCMAudio(url2)
            vc.play(source)

    @commands.command(name="pause", description="Pauses the song.")
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.reply("Paused the current song.")

    @commands.command(name="resume", description="Resumes the song.")
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.reply("Resumed the current song.")
    
    
    





def setup(bot):
    bot.add_cog(Music(bot))