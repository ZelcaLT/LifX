import datetime
import json
import os
import aiofiles
import nextcord
import aiosqlite
import sys
import aiohttp
import urllib
import asyncio
from nextcord.ext import ipc, commands
from io import BytesIO






class Admin(commands.Cog, name="⚙Admin"):

    def __init__(self, bot):
        self.bot = bot


        
    """Cogs for moderation and owner only"""

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")
   
    @commands.command(name="slowmode", description="Sets the slowmode for a channel.")
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, time:int):
        try:
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

        except Exception:
            print("Error in slowmode command!")


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

            

    @commands.command(name="tempmute", description="Temp-mutes a user for a specified amount of time.")
    @commands.has_permissions(manage_messages=True)
    async def tempmute(self, ctx, member : nextcord.Member, time:int , reason=None):
        if ctx.author.guild.id == 921758771158605834:
            mod_logging = self.bot.get_channel(922276099147313174)
            guild = ctx.guild
            if reason == None:
                reason = "Not specified"
            muted_role = nextcord.utils.get(guild.roles, name="Muted")
            await member.add_roles(muted_role, reason=reason)

            e = nextcord.Embed(
                title="Member muted",
                description=f"{member.mention} was muted\nReason: {reason}\nDuration: {time} seconds",
                color=nextcord.Colour.blurple()
            )
            await mod_logging.send(embed=e)

            await asyncio.sleep(time)
            await member.remove_roles(muted_role, reason=reason)

            e2 = nextcord.Embed(
                title="Member unmuted",
                description=f"{member.mention} was unmuted\nDuration: {time} seconds",
                color=nextcord.Colour.blurple()
            
            )
            await mod_logging.send(embed=e2)
        

    @tempmute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("You need to mention a member/You require time in seconds")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply("You need permission to mute this member")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("You need to put the command in the correct format")







    


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


    @commands.command(name="test", description="A testing command.")
    async def test(self, ctx):
        await ctx.send("testing lol\nsup nerds")

    @commands.Cog.listener()
    async def on_member_join(self, member): 
        if member.guild.id == 921758771158605834:
            e = nextcord.Embed(
                title="Member joined server",
                description=f"{member.mention} has joined the server.",
                color=nextcord.Colour.green()
            )
            e.add_field(name="Name:", description=f"{member.name}", inline=False)
            e.add_field(name="ID:", description=f"{member.id}", inline=False)
            e.add_field(name="Created at:", description=f"{member.created_at}", inline=False)
            if member.bot is True:
                e.add_field(name="Bot:", description=f"Is bot", inline=False)
            else:
                e.add_field(name="Bot:", description=f"Is not bot", inline=False)

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