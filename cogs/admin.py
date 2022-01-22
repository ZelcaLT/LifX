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
from nextcord.ext.commands import Cog, Context, command


from models.infraction import Infraction, InfractionType
from helpers.checks import STAFF, is_staff




class Admin(commands.Cog, name="⚙Admin"):
    """Admin/Mod commands"""
    def __init__(self, bot):
        self.bot = bot

    async def create_infraction(self, ctx: Context, member: Member, type: int, reason: str) -> bool:
        if not reason:
            await ctx.send(":x: You must provide a reason for moderation actions.")
            return False

        if STAFF in member._roles:
            await ctx.reply("You cannot infract staff members.")
            return False

        infraction = await Infraction.new(self.bot.db, member, ctx.author, type, reason)  # type: ignore
        await ctx.reply(content="Infraction created!", embed=infraction.embed)

        return True

    @staticmethod
    async def try_dm(member: Member, message: str) -> bool:
        try:
            await member.send(message)
        except DiscordException:
            return False
        return True

    @command(name="note")
    @is_staff()
    async def note(self, ctx: Context, member: Member, *, reason: str) -> None:
        """Create a note on a user."""

        await self.create_infraction(ctx, member, InfractionType.NOTE, reason)

    @command(name="warn")
    @is_staff()
    async def warn(self, ctx: Context, member: Member, *, reason: str) -> None:
        """Warn a user."""

        if not await self.create_infraction(ctx, member, InfractionType.WARN, reason):
            return

        await self.try_dm(member, f"You have been warned in The Coders: {reason}")

    @command(name="kick")
    @is_staff()
    async def kick(self, ctx: Context, member: Member, *, reason: str) -> None:
        """Kick a user."""

        if not await self.create_infraction(ctx, member, InfractionType.KICK, reason):
            return

        await self.try_dm(member, f"You have been kicked from The Coders: {reason}")
        await member.kick(reason=reason)

    @command(name="ban")
    @is_staff()
    async def ban(self, ctx: Context, member: Member, *, reason: str) -> None:
        """Ban a user."""

        if not await self.create_infraction(ctx, member, InfractionType.BAN, reason):
            return

        await self.try_dm(member, f"You have been banned from The Coders: {reason}")
        await member.ban(reason=reason)

    @command(name="unban")
    @is_staff()
    async def unban(self, ctx: Context, member: int) -> None:
        """Unban a user."""

        try:
            user = await self.bot.fetch_user(member)
        except DiscordException:
            await ctx.reply("API Error: Invalid user.")
            return

        await ctx.guild.unban(user)  # type: ignore
        await ctx.reply("Member has been unbanned.")

    @command(name="cases")
    @is_staff()
    async def cases(self, ctx: Context, member: Union[Member, int]) -> None:
        """Get cases for a user."""

        if isinstance(member, Member):
            member = member.id

        cases = await Infraction.find_member_infractions(self.bot.db, member)

        if not cases:
            await ctx.reply("No cases were found for that user.")
            return

        content = "\n".join([case.short for case in cases])

        embed = Embed(
            title=f"Cases for {member}",
            description=content,
            colour=0x87CEEB,
        )

        await ctx.reply(embed=embed)

    @command(name="case")
    @is_staff()
    async def case(self, ctx: Context, id: int) -> None:
        """Get details about a specific case."""

        case = await Infraction.find_infraction(self.bot.db, id)

        if not case:
            await ctx.reply("There is no case with that ID.")
            return

        await ctx.reply(embed=case.embed)

    


    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")

    @commands.command(name="mute", description="'Timeouts' a member. (specific to premium)")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: nextcord.Member,time:int, *, reason=None):
        if ctx.guild.id == 921758771158605834:
            mute = ctx.guild.get_role(922857417610522674)
            everyone = ctx.guild.get_role(922271084890423339)
            author = ctx.author

            await member.add_roles(mute)
            await member.remove_roles(everyone)
            em = Embed(
                title="Muted",
                description=f"You have been muted in `The Coders` | Reason: {reason} | Duration: {time}",
                color=nextcord.Colour.red()
            )
            await member.send(embed=em)
            await ctx.reply(f"Muted {member.mention} | Reason: {reason} | Duration: {time}")

            await asyncio.sleep(time)
            await member.remove_roles(mute)
            await member.add_roles(everyone)

            em1 = Embed(
                title="Unmuted",
                description=f"You have been unmuted in `The Coders` | Reason: Auto-unmute",
                color=nextcord.Colour.green()
            )
            await member.send(embed=em1)
        
        else:
            await ctx.reply("This command is for premium members only!")




   
    @commands.command(name="slowmode", description="Sets the slowmode for a channel.")
    @commands.has_permissions(manage_messages=True)
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



    @commands.command(name="purge", description="Clears messages.")
    @commands.has_permissions(manage_messages=True)
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

    @commands.command(name="kick", description="Kicks someone from the guild.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, mem:nextcord.Member, *, reason=None):
        if reason is None:
            reason = "No reason given"
        await ctx.guild.kick(mem, reason=reason)


    @commands.command(name="steal", description="Steals an emoji from an another server.")
    @commands.has_permissions(manage_messages=True)
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


    @commands.command(name="strike", description="'Strikes' a user for breaking the rules.")
    @commands.has_permissions(manage_messages=True)
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
    async def on_message_delete(self, message_before):
        if message_before.guild.id == 921758771158605834:
            emb = nextcord.Embed(
                title=f"{message_before.author.name} has deleted a message | {message_before.author.id}",
                description=f"**Content:**\n{message_before.content}\n**Channel:**\n<#{message_before.channel.id}>",
                color =nextcord.Colour.dark_red()
            )
            if message_before.author.bot:
                return
            else:
                mod_logging = self.bot.get_channel(922276099147313174)
                await mod_logging.send(embed=emb)
        
        

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



    @commands.command(name="adminMeme", description="Shows the meme for the day.")
    @commands.has_permissions(manage_messages=True)
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