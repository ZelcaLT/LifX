import datetime
import os 
import aiofiles
import pickle
import nextcord
import aiosqlite
import urllib
import asyncio
import time
import random
from nextcord.ext import ipc, commands
from nextcord.ext.commands.cooldowns import BucketType


class Utility(commands.Cog, name="🔌Utility"):
    def __init__(self, bot):
        self.bot = bot




    @commands.command(name="serverinfo", description="Shows details about the server.")
    @commands.cooldown(1, 60, BucketType.member)
    async def serverinfo(self, ctx):
        roles1 = len(ctx.guild.roles)

        e = nextcord.Embed(timestamp=ctx.message.created_at, color=ctx.author.color)
        e.add_field(name="Name", value=f"{ctx.guild.name}", inline=False)
        e.add_field(name="Member Count", value=ctx.guild.member_count)
        e.add_field(name="Verification level", value=str(ctx.guild.verification_level))
        e.add_field(name="Highest role", value=f"<{ctx.guild.roles[-1]}")
        e.add_field(name="Number of Roles", value=str(roles1))
        e.add_field(name="Nitro boosts", value=f"{ctx.guild.premium_subscription_count}")
        e.add_field(name="Created at", value=f"{ctx.guild.created_at} UTC")
        e.add_field(name="ID", value=f"{ctx.guild.id}")
        e.add_field(name="Owner", value=f"{ctx.guild.owner}")
        e.add_field(name="Nitro level", value=f"{ctx.guild.premium_tier}")
        e.set_thumbnail(url=ctx.guild.icon)

        await ctx.reply(embed=e)


    @commands.command()
    @commands.cooldown(1, 1800, BucketType.member) 
    async def ticket(self, ctx):
        guild = ctx.guild
        Role1 = ctx.guild.get_role(922228778279763968)
        if ctx.author.guild.id == 921758771158605834:
            overwrites = {
                guild.default_role: nextcord.PermissionOverwrite(
                    read_messages=False,
                    send_messages=False,
                ),
                Role1: nextcord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                ),
                ctx.author: nextcord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                )

                }
            TicketChannel = await guild.create_text_channel(name=f"{ctx.author.display_name}_ticket", overwrites=overwrites)
            await ctx.send(f"Created ticket. Head to <#{TicketChannel.id}>.")
            e = nextcord.Embed(title="Ticket", description=f"Welcome to your ticket. Please state your issue/feedback and we'll get back to you.\n")
            e.set_image(url="https://preview.redd.it/z02scgtydp121.gif?format=mp4&s=7651d6f6d327bb6ae8c6d60811d2a598bb8c54c5")
            await TicketChannel.send(embed=e)
            await TicketChannel.send("[ <@&922228778279763968> ]")

        


    @commands.command()
    async def ping(self, ctx):
        em = nextcord.Embed(
            title="Pong!🏓",
            description=f"🏓 {round(self.bot.latency * 1000)}ms",
            color=nextcord.Colour.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        await ctx.reply(embed=em)


    @commands.command()
    async def info(self, ctx):
        e = nextcord.Embed(
            title="Info",
            description=f"Made by `ZxlcaLT#0001`\nPrefix: `*`\nSupport server: [Click](https://discord.gg/haRQahMR4V \"Support Server\")"
        )


        e.add_field(name="Changelog",value="```diff\n- Added 'tag' command to 'tags.py'\n- Changed prefix to '=='```")
        await ctx.reply(embed=e)
    



    @commands.command(name="invite", description="Shows a permanent invite for the support server and the bots invite.")
    async def invite(self, ctx):
        botInv = "https://discord.com/oauth2/authorize?client_id=922489691020873758&permissions=8&scope=bot%20applications.commands"
        serverInv = "https://discord.gg/haRQahMR4V"
        embed = nextcord.Embed(
            title="Links",
            description=f"Bot invite: {botInv}\nSupport server invite: {serverInv}",
            color = nextcord.Colour.blurple()
        )
        await ctx.reply(embed=embed)







def setup(bot):
    bot.add_cog(Utility(bot))