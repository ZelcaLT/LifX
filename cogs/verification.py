import datetime
import os 
import aiofiles
import pickle
import nextcord
import aiosqlite
import asyncio
import urllib
import random
from nextcord.embeds import EmptyEmbed
from nextcord.ext import ipc, commands
from nextcord.ext.commands.cooldowns import BucketType


class Verify(commands.Cog, name="✅Verify"):
    """Verify in **./syntax**"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 921758771158605834:
            if not member.bot:
                channel = nextcord.utils.get(self.bot.get_all_channels(), guild__name='./syntax', name='verify-here')
                emb = nextcord.Embed(
                    title=f"Welcome {member.display_name}",
                    description="Verify by doing the command `==verify` in this channel to get access to the server.\nMake sure to read the rules! <#921760273637998642>\nThis message will auto-delete in 2 minutes.",
                    color=nextcord.Colour.random()
                )
                emb.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=emb, delete_after=120)
                await channel.send(f"[{member.mention}]")
                chan = nextcord.utils.get(self.bot.get_all_channels(), guild__name="./syntax", name="chat")
                await chan.send(f":wave: Welcome {member.mention}!")
                

    @commands.command(name="verify", description="Verify yourself for access to the server.")
    async def verify(self, ctx):
        if ctx.author.guild.id == 921758771158605834:
            if ctx.channel.id == 921760303513993267:
                if not ctx.author.bot:
                    verifiedRole = nextcord.utils.get(ctx.guild.roles, name="Verified")
                    e = nextcord.Embed(
                        title="Verification",
                        description="Verify by saying `confirm` and you will be granted access to the server",
                        color=nextcord.Colour.random()
                    )




                    msg = await ctx.reply(embed=e, delete_after=10)

                    # we define a local variable named 'correct_answer'
                    correct_answers = 'confirm'

                    
                    def check(message : nextcord.Message) -> bool: 
                        return message.author == ctx.author and message.content == correct_answers

                    try:
                        message = await self.bot.wait_for('message', timeout = 30, check = check)

                # this will be executed if the user took too long to answer
                    except asyncio.TimeoutError: 
                        await ctx.reply("Error: timed out\nPlease re-verify by using `==verify`")           

                # this will be executed if the author responded properly
                    else: 
                        await ctx.author.add_roles(verifiedRole)
                        await ctx.author.send(f"You were verified in `{ctx.guild.name}`")
                        

                # this will be executed regardless
                    finally: 
                        pass
            else:
                await ctx.reply("You can't verify in this channel!")
        else:
            return await ctx.reply("You can't verify in this server!'")







def setup(bot):
    bot.add_cog(Verify(bot))