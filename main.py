import asyncio
import datetime
import os 
import aiohttp
import aiofiles
import nextcord
from nextcord.embeds import EmptyEmbed
from nextcord.ext import ipc, commands, menus
import aiosqlite
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.keys import Keys
import re
import config
from urllib.parse import unquote
import json
import math
import urllib
import random
import time


intents = nextcord.Intents.default()


class myBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


bot = myBot(command_prefix=commands.when_mentioned_or(config.prefix), intents=intents)
bot.remove_command("help")




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

    statuses = [f"{config.prefix}help",f"{len(bot.guilds)} servers"]

    while not bot.is_closed():

        status = random.choice(statuses)

        await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=status))

        await asyncio.sleep(5)

bot.loop.create_task(ch_pr())




class HelpPageSource(menus.ListPageSource):
    def __init__(self, help_command, data):
        self._help_command = help_command
        # you can set here how many items to display per page
        super().__init__(data, per_page=2)

    async def format_page(self, menu, entries):
        """
        Returns an embed containing the entries for the current page
        """
        prefix = self._help_command.context.clean_prefix
        invoked_with = self._help_command.invoked_with
        embed = nextcord.Embed(title="Bot Commands",
                               colour=self._help_command.COLOUR)
        embed.description = (
            f'Use "{prefix}{invoked_with} command" for more info on a command.\n'
            f'Use "{prefix}{invoked_with} category" for more info on a category.'
        )
        # add the entries to the embed
        for entry in entries:
            embed.add_field(name=entry[0], value=entry[1], inline=True)
        # set the footer to display the page number
        embed.set_footer(
            text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed

class HelpButtonMenuPages(menus.ButtonMenuPages):

    FIRST_PAGE = "<:pagefirst:899973860772962344>"
    PREVIOUS_PAGE = "<:pageprev:899973860965888010>"
    NEXT_PAGE = "<:pagenext:899973860840050728>"
    LAST_PAGE = "<:pagelast:899973860810694686>"
    STOP = "<:stop:899973861444042782>"

    def __init__(self, ctx: commands.Context, **kwargs):
        super().__init__(**kwargs)
        self._ctx = ctx

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        """Ensure that the user of the button is the one who called the help command"""
        return self._ctx.author == interaction.user


class NewHelpCommand(commands.MinimalHelpCommand):
    """Custom help command override using embeds"""

    # embed colour
    COLOUR = nextcord.Colour.blurple()

    def get_command_signature(self, command: commands.core.Command):
        """Retrieves the signature portion of the help page."""
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping: dict):
        """implements bot command help page"""
        prefix = self.context.clean_prefix
        invoked_with = self.invoked_with
        embed = nextcord.Embed(title="Bot Commands", colour=self.COLOUR)
        avatar = self.context.bot.user.avatar
        avatar_url = avatar.url if avatar else EmptyEmbed
        embed.set_author(name=self.context.bot.user.name, icon_url=avatar_url)
        embed.description = (
            f'Use "{prefix}{invoked_with} command" for more info on a command.\n'
            f'Use "{prefix}{invoked_with} category" for more info on a category.'
        )

        embed_fields = []

        for cog, commands in mapping.items():
            name = "No Category" if cog is None else cog.qualified_name
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                # \u2002 = en space
                value = "\u2002".join(
                    f"`{c.name}`" for c in filtered)
                if cog and cog.description:
                    value = f"{cog.description}\n{value}"
                # add (name, value) pair to the list of fields
                embed_fields.append((name, value))

        # create a pagination menu that paginates the fields
        pages = HelpButtonMenuPages(
            ctx=self.context,
            source=HelpPageSource(self, embed_fields),
            disable_buttons_after=True
        )
        await pages.start(self.context)

    async def send_cog_help(self, cog: commands.Cog):
        """implements cog help page"""
        embed = nextcord.Embed(
            title=f"{cog.qualified_name} Commands", colour=self.COLOUR
        )
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(
                name=self.get_command_signature(command),
                value=command.short_doc or "...",
                inline=False,
            )

        embed.set_footer(
            text=f"Use {self.context.clean_prefix}help [command] for more info on a command.")
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group: commands.Group):
        """implements group help page and command help page"""
        embed = nextcord.Embed(title=group.qualified_name, colour=self.COLOUR)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.short_doc or "...",
                    inline=False,
                )

        await self.get_destination().send(embed=embed)

    # Use the same function as group help for command help
    send_command_help = send_group_help


bot.help_command = NewHelpCommand()


"""
    Main python run file
""" 

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

    
    


@bot.event
async def on_ready():
    print(bot.user.name + " is ready.\n============================")


    
3


bot.run(config.token)