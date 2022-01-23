import asyncio
import datetime
import os
from typing import Optional, Set 
import aiohttp
import aiofiles
import nextcord
from nextcord.embeds import EmptyEmbed
from nextcord.ext import ipc, commands, menus
import aiosqlite
import re
import config
from urllib.parse import unquote
from nextcord import Embed
import json

import math
import sys
import urllib
import random
import time


intents = nextcord.Intents.all()

class myBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

async def get_prefix(bot, message):
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (message.guild.id))
            data = await cursor.fetchone()
            if data:
                return data
            else:
                try:
                    await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (?, ?)', ('==', message.guild.id))
                    await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (message.guild.id))
                    data = cursor.fetchone()
                    if data:
                        await cursor.execute('UPDATE prefixes SET prefix = ? WHERE guild = ? ', ('==', message.guild.id))
                except Exception:
                    return '=='

bot = myBot(command_prefix="==", intents=intents)
bot.remove_command("help")
bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"

@bot.command()  
@commands.is_owner()
async def guild(ctx):
    em = nextcord.Embed(title="Guilds")
    for guild in bot.guilds:
        em.add_field(name=f"{guild.name}", value="cool")
        
    await ctx.reply(embed=em)


class CodeButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red)
    async def delete(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Deleting thread...", ephemeral=True)
        self.value = True
        self.stop()




async def ch_pr():
    await bot.wait_until_ready()

    statuses = [f"{config.prefix}help",f"{len(bot.guilds)} servers",f"on {config.version}"]

    while not bot.is_closed():

        status = random.choice(statuses)

        await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=status))

        await asyncio.sleep(5)

bot.loop.create_task(ch_pr())




 

class HelpDropdown(nextcord.ui.Select):
    def __init__(self, help_command: "MyHelpCommand", options: list[nextcord.SelectOption]):
        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)
        self._help_command = help_command

    async def callback(self, interaction: nextcord.Interaction):
        embed = (
            await self._help_command.cog_help_embed(self._help_command.context.bot.get_cog(self.values[0]))
            if self.values[0] != self.options[0].value
            else await self._help_command.bot_help_embed(self._help_command.get_bot_mapping())
        )
        await interaction.response.edit_message(embed=embed)


class HelpView(nextcord.ui.View):
    def __init__(self, help_command: "MyHelpCommand", options: list[nextcord.SelectOption], *, timeout: Optional[float] = 120.0):
        super().__init__(timeout=timeout)
        self.add_item(HelpDropdown(help_command, options))
        self._help_command = help_command

    async def on_timeout(self):
        # remove dropdown from message on timeout
        self.clear_items()
        await self._help_command.response.edit(view=self)

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        return self._help_command.context.author == interaction.user


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"{command.qualified_name} {command.signature}"

    async def _cog_select_options(self) -> list[nextcord.SelectOption]:
        options: list[nextcord.SelectOption] = []
        options.append(nextcord.SelectOption(
            label="Home",
            emoji="🏠",
            description="Go back to the main menu.",
        ))

        for cog, command_set in self.get_bot_mapping().items():
            filtered = await self.filter_commands(command_set, sort=True)
            if not filtered:
                continue
            emoji = getattr(cog, "COG_EMOJI", None)
            options.append(nextcord.SelectOption(
                label=cog.qualified_name if cog else "No Category",
                emoji=emoji,
                description=cog.description[:100] if cog and cog.description else None
            ))

        return options

    async def _help_embed(
        self, title: str, description: Optional[str] = None, mapping: Optional[str] = None,
        command_set: Optional[Set[commands.Command]] = None, set_author: bool = False
    ) -> nextcord.Embed:
        embed = nextcord.Embed(title=title, color=nextcord.Colour.random())
        if description:
            embed.description = description
        if set_author:
            avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
            embed.set_author(name=self.context.bot.user.name, icon_url=avatar.url)
        if command_set:
            # show help about all commands in the set
            filtered = await self.filter_commands(command_set, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.description or "...",
                    inline=True
                )
        elif mapping:
            # add a short description of commands in each cog
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort=True)
                if not filtered:
                    continue
                name = cog.qualified_name if cog else "❓Other"
                emoji = getattr(cog, "COG_EMOJI", None)
                cog_label = f"{emoji} {name}" if emoji else name
                # \u2002 is an en-space
                cmd_list = "\u2002".join(
                    f"`{cmd.name}`" for cmd in filtered
                )
                value = (
                    f"{cog.description}\n{cmd_list}"
                    if cog and cog.description
                    else cmd_list
                )
                embed.add_field(name=cog_label, value=value)
        return embed

    async def bot_help_embed(self, mapping: dict) -> nextcord.Embed:
        return await self._help_embed(
            title="Bot Commands",
            description=self.context.bot.description,
            mapping=mapping,
            set_author=True,
        )
    
    async def send_bot_help(self, mapping: dict):
        embed = await self.bot_help_embed(mapping)
        options = await self._cog_select_options()
        self.response = await self.get_destination().send(embed=embed, view=HelpView(self, options))

    async def send_command_help(self, command: commands.Command):
        emoji = getattr(command.cog, "COG_EMOJI", None)
        embed = await self._help_embed(
            title=f"{emoji} {command.qualified_name}" if emoji else command.qualified_name,
            description=command.description,
            command_set=command.commands if isinstance(command, commands.Group) else None
        )
        await self.get_destination().send(embed=embed)

    async def cog_help_embed(self, cog: Optional[commands.Cog]) -> nextcord.Embed:
        if cog is None:
            return await self._help_embed(
                title=f"No category",
                command_set=self.get_bot_mapping()[None]
            )
        emoji = getattr(cog, "COG_EMOJI", None)
        return await self._help_embed(
            title=f"{emoji} {cog.qualified_name}" if emoji else cog.qualified_name,
            description=cog.description,
            command_set=cog.get_commands()
        )

    async def send_cog_help(self, cog: commands.Cog):
        embed = await self.cog_help_embed(cog)
        await self.get_destination().send(embed=embed)

    # Use the same function as command help for group help
    send_group_help = send_command_help

bot.help_command = MyHelpCommand()

@bot.slash_command(name="test", description="A testing command.")
async def test(ctx):
    await ctx.send("testing lol\nsup nerds")


"""
    Main python run file
""" 
try:
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


except Exception as e:
    print(f"{e}")
            



    


bot.run(config.token)