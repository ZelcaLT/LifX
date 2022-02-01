ces = [
    "shit",
    "dick",
    "fuck",
    "die",
    "kys",
    "d1e",
    "f4ck",
    "cum",
    "c0m",
    "cvm",
    "f4ck",
    "cunt",
    "ass",
    "a$$",
    "asshole",
    "a$$hole"
    ]
import datetime
import json
import os
from pydoc import describe
from typing import Union
import aiofiles
import nextcord
import aiosqlite
import sys
import humanfriendly
import aiohttp
import urllib
from nextcord import Embed
import asyncio
from nextcord.ext import ipc, commands
from io import BytesIO

from nextcord import Member, DiscordException, Embed
from nextcord.ext.commands import Cog, Context, command, has_permissions
from nextcord.utils import get as g


from models.infraction import Infraction, InfractionType
from helpers.checks import STAFF, is_staff



s = 922228778279763968

class Admin(commands.Cog, name="⚙Admin"):
    """Admin/Mod commands"""
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 921758771158605834:
            if not message.author.bot:
                if not g(message.author.roles, id=s):
                    for word in ces:
                        if word in message.content:
                           
                            chan = self.bot.get_channel(934914628335591455)
                            await message.delete()
                            em = Embed(
                                title="Automoderation",
                                description=f"I deleted a message that contained bad language.\nFrom: {message.author.mention}",
                                color=nextcord.Colour.red()
                            )
                            em.add_field(name="Message content", value=f"{message.content}", inline=False)
                            em.add_field(name="In channel", value=f"{message.channel.mention}", inline=False)
                            em.add_field(name="Message ID", value=f"{message.id}", inline=False)
                            await chan.send(embed=em)

        
    


    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")

    @command(name="mute", description="'Timeouts' a member. (specific to premium)")
    @has_permissions(manage_messages=True)
    async def mute(self, ctx, member: nextcord.Member,time:int, *, reason=None):
        if ctx.guild.id == 921758771158605834:
            mute = ctx.guild.get_role(922857417610522674)
            everyone = ctx.guild.get_role(922271084890423339)
            author = ctx.author

            await member.add_roles(mute)
            await member.remove_roles(everyone)
            em = Embed(
                title="Muted",
                description=f"You have been muted in `./syntax` | Reason: {reason} | Duration: {time}",
                color=nextcord.Colour.red()
            )
            await member.send(embed=em)
            await ctx.reply(f"Muted {member.mention} | Reason: {reason} | Duration: {time}")

            await asyncio.sleep(time)
            await member.remove_roles(mute)
            await member.add_roles(everyone)

            em1 = Embed(
                title="Unmuted",
                description=f"You have been unmuted in `./syntax` | Reason: Auto-unmute",
                color=nextcord.Colour.green()
            )
            await member.send(embed=em1)
        
        else:
            await ctx.reply("This command is for premium members only!")




   
    @command(name="slowmode", description="Sets the slowmode for a channel.")
    @has_permissions(manage_messages=True)
    async def slowmode(self, ctx, time:int):

        if time == 0:
            await ctx.message.delete()
            await ctx.channel.edit(slowmode_delay = time)
            e = nextcord.Embed(
                title="Slowmode change",
                description=f"Slowmode off for {ctx.channel}\nDelay: {time} seconds\nResponsible moderator: {ctx.author.mention}", 
                color=nextcord.Colour.random()
            )
            msg = await ctx.send(embed=e)
            mod_logging = self.bot.get_channel(922276099147313174)
            await mod_logging.send(embed=e)
            await asyncio.sleep(10)
            await msg.delete()
        elif time > 21600:
            await ctx.message.delete()
            e = nextcord.Embed(
                title="Error!",
                description=f"You cannot change the slowmode to above 6 hours!", 
                color=nextcord.Colour.red()
            )
            msg = await ctx.send(embed=e)
            mod_logging = self.bot.get_channel(922276099147313174)
            await mod_logging.send(embed=e)
            await asyncio.sleep(10)
            await msg.delete()
        else:
            await ctx.channel.edit(slowmode_delay = time)
            await ctx.message.delete()
            e = nextcord.Embed(
                title="Slowmode change",
                description=f"Slowmode turned on for {ctx.channel}\nDelay: {time} seconds\nResponsible moderator: {ctx.author.mention}", 
                color=nextcord.Colour.random()
            )
            msg = await ctx.send(embed=e)
            mod_logging = self.bot.get_channel(922276099147313174)
            await mod_logging.send(embed=e)
            await asyncio.sleep(10)
            await msg.delete()



    @command(name="purge", description="Clears messages.")
    @has_permissions(manage_messages=True)
    async def purge(self,ctx,number:int=None):
        if number == None or 0:
            return await ctx.send("I need a number of messages to purge!")
        await ctx.message.delete()
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=number)
        e = nextcord.Embed(
            title="Purged",
            description=f"Purged {number} message(s) in channel <#{ctx.channel.id}>\nModerator: {ctx.author.mention}",
            color=nextcord.Colour.red()
        )
        msg = await ctx.send(embed=e)
        mod_logging = self.bot.get_channel(922276099147313174)
        await mod_logging.send(embed=e)
        await asyncio.sleep(10)
        await msg.delete()

    @command(name="kick", description="Kicks someone from the guild.")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, mem:nextcord.Member, *, reason=None):
        if reason is None:
            reason = "No reason given"
        await ctx.guild.kick(mem, reason=reason)


    @command(name="steal", description="Steals an emoji from an another server.")
    @has_permissions(manage_messages=True)
    async def steal(self, ctx, url:str, *, name=None):
        guild=ctx.guild.id
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    imgOrGif = BytesIO(await r.read())
                    bValue = imgOrGif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=bValue, name=name)
                        await ctx.send(f"Emoji {name} added")
                        await ses.close()
                    else:
                        await ctx.send(f"This did not work. | {r.status}")
                except nextcord.HTTPException:
                    await ctx.send("file = too thicc for me to handle")


    @command(name="strike", description="'Strikes' a user for breaking the rules.")
    @has_permissions(manage_messages=True)
    async def strike(self, ctx, member : nextcord.Member, *, reason =None):
        mod_logging = self.bot.get_channel(922276099147313174)
        if member == ctx.author:
            await ctx.send("You can\'t strike yourself!")
            return
        if member.bot:
            await ctx.send("You can\'t strike a bot!")
            return
        db_name = "warn.db"
        db = await aiosqlite.connect(db_name)
        cursor = await db.cursor()

        if reason == None:
            reason = "No reason specified"

        if ctx.guild.id == 921758771158605834:
            e = nextcord.Embed(
                title="Member striked",
                color=nextcord.Colour.red()
            )
            e.add_field(name="Member", value=member.mention)
            e.add_field(name="Member ID", value=member.id)
            e.add_field(name="Reason", value=reason)
            e.add_field(name="Responsible moderator", value=ctx.author.mention)
            await mod_logging.send(embed=e)


        await cursor.execute("CREATE TABLE IF NOT EXISTS warn(guild_id STR, user_id STR , warn_num STR, PRIMARY KEY (guild_id, user_id))")
        await db.commit()

        await cursor.execute("SELECT * FROM warn WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id))
        data = await cursor.fetchone()

        

        if data is None:
            await cursor.execute("INSERT INTO warn(guild_id, user_id, warn_num) VALUES(?,?,?)", (ctx.guild.id, member.id, str(1)))
            await db.commit()
            await ctx.send(f"{member.mention} is striked for the first time\nReason: {reason}")
            return
        



        else:
            await cursor.execute("UPDATE warn SET warn_num = warn_num + ? WHERE guild_id = ? AND user_id = ?", (str(1), ctx.guild.id, member.id))
            await db.commit()
            await cursor.execute("SELECT warn_num FROM warn WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id))
            data2 = await cursor.fetchone()
            final = data2[0]
            print(final)
            await ctx.send(f"{member.mention} has been striked {final} times\nReason: {reason}")
            return

            






    


 
        

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.author.guild.id == 921758771158605834:
            emb = nextcord.Embed(
                title=f"{message_before.author.name} has edited a message | {message_before.author.id}",
                description=f"**Channel:**\n<#{message_before.channel.id}>",
                color =nextcord.Colour.dark_red()
            )
            emb.add_field(name="Before:", value=f"{message_before.content}", inline=False)
            emb.add_field(name="After:", value=f"{message_after.content}", inline=False)
            if message_after.author.bot:
                return
            else:
                mod_logging = self.bot.get_channel(922276099147313174)
                await mod_logging.send(embed=emb)




    @commands.Cog.listener()
    async def on_member_join(self, member): 
        if member.guild.id == 921758771158605834:
            e = nextcord.Embed(
                title="Member joined server",
                description=f"{member.mention} has joined the server.",
                color=nextcord.Colour.green()
            )
            e.add_field(name="Name:", value=f"{member.name}", inline=False)
            e.add_field(name="ID:", value=f"{member.id}", inline=False)
            e.add_field(name="Created at:", value=f"{member.created_at}", inline=False)
            if member.bot is True:
                e.add_field(name="Bot:", value=f"Is bot", inline=False)
            else:
                e.add_field(name="Bot:", value=f"Is not bot", inline=False)

            await self.bot.get_channel(922276099147313174).send(embed=e)



    @command(name="adminMeme", description="Shows the meme for the day.")
    @has_permissions(manage_messages=True)
    async def adminMeme(self, ctx):
        await ctx.message.delete()
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
        await ctx.send(embed=embed)
        await ctx.send("<@&921798446128701461>")










def setup(bot):
    bot.add_cog(Admin(bot))