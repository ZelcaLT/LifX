import datetime
import os 
import aiofiles
import pickle
import nextcord
import aiosqlite
import urllib
import random
from nextcord.ext import ipc, commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext.commands.cooldowns import BucketType
from nextcord.mentions import A


class Program(commands.Cog, name="💻Python Tags"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")
        
    testServer = 921758771158605834

    @commands.group(name="tag", description="group")
    async def tag(self, ctx):
        if ctx.invoked_subcommand is None:
            cog = Program(self)
            command = cog.get_commands()
            e = nextcord.Embed(
                title=f"List of tags", 
                description=f"```{[c.qualified_name for c in cog.walk_commands()]}```",
                color=nextcord.Colour.random()
            )
            await ctx.reply(embed=e)

        
    @tag.command(name="path")
    async def path(self, ctx):
        e = nextcord.Embed(
            title="PATH", 
            description="If you get an error message saying that 'pip' or 'python' \"is not recognized as an internal or external command\", or something similar, you might have not adjusted your PATH system variable to include the executable paths pointing to either program. Alternatively, you may need to activate your virtual environment and use python -m pip ... instead.",
            color=nextcord.Colour.random()
            )
        e.add_field(name="How to adjust PATH on Windows:", value="https://www.computerhope.com/issues/ch000549.htm")
        e.add_field(name="How to adjust PATH on Unix:", value="https://unix.stackexchange.com/questions/26047/how-to-correctly-add-a-path-to-path/26059#26059")
        e.add_field(name="How to adjust PATH on Mac:", value="https://www.architectryan.com/2012/10/02/add-to-the-path-on-mac-os-x-mountain-lion/")
        await ctx.reply(embed=e)
    
    @tag.command(name="emoji")
    async def emoji(self, ctx):
        e = nextcord.Embed(
            title="Emojis for bots:",
            description=f"Custom emotes are represented internally in the following format: <:name:id>\nWhere the name is the name of the custom emote, and the ID is the id of the custom emote.\nFor example, <:python3:232720527448342530> is the name:id for :python3:\nWhen sending standard unicode/discord emojis, you just send the unicode character.\nYou can quickly obtain the <:name:id> format by putting a backslash in front of the custom emoji when you put it in your client.\n\nExample: \:python3: would give you the <:name:id> format.\n\nAnimated emojis are the same as above but have an a before the name- `ie: <a:name:id>`",
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)

    @tag.command(name="lp")
    async def lp(self, ctx):
        e = nextcord.Embed(
            title="Learn Python",
            description="https://docs.python.org/3/tutorial/ (official tutorial)\nhttp://python.swaroopch.com/ (useful book)\nhttps://automatetheboringstuff.com/ (for complete beginners to programming)\nhttp://greenteapress.com/wp/think-python-2e/ (another decent book)\nSee also: \nhttp://www.codeabbey.com/ (exercises for beginners)\nhttps://realpython.com/ (good articles on specific topics)\nhttps://learnxinyminutes.com/docs/python3/ (cheatsheet)",
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)

    @tag.command(name="help")
    async def help(self, ctx):
        if ctx.author.guild.id == 921758771158605834:
            await ctx.reply("Please refer to **AFH Rule 5**")

    @tag.command(name="shard")
    async def shard(self, ctx):
        e = nextcord.Embed(
            title="To shard your bot:",
            description="```py\nbot = commands.AutoShardedBot(command_prefix=[your_prefix], description=\"An AutoShardedBot.```\n**What is it?**\nSharding is a nice way to split your bot to smaller, more manageable parts. It is recommended to only use this feature with big bots (1000 guilds or more).\nNote that you are required to use this when your bot reaches 2000+ guilds.\nDocs: https://nextcord.readthedocs.io/en/latest/ext/commands/api.html#nextcord.ext.commands.AutoShardedBot",
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)

    @tag.command(name="cogs")
    async def cogs(self, ctx):
        e = nextcord.Embed(
            title="Cogs",
            description="There comes a point in your bot's development when you want to organize a collection of commands, listeners, and some state into one class. Cogs allow you to do just that.\nAn example of a cog:\n```py\nimport nextcord\nfrom nextcord.ext import commands\n\nclass ...(commands.Cog, name=\"...\"):\n    def __init__(self, bot):\n        self.bot = bot```\n\nGithub example: https://github.com/TheCodersYT/Nextcord-Examples/blob/main/examples/cog.py",
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)

    @tag.command(name="diswarn")
    async def diswarn(self, ctx):
        e = nextcord.Embed(
            title="Distribution Warning Fix:",
            description="If you get an error like this when you start your bot: `DistributionWarning: discord.py is installed which is incompatible with nextcord`, then you have not uninstalled discord.py when you installed nextcord.\nTo uninstall discord.py, use the command (in terminal)`pip uninstall discord.py`",
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)

    @tag.command(name="command")
    async def command(self, ctx):
        e = nextcord.Embed(
            title="Command Example",
            description="A command is a way of reciv"
        )
            







def setup(bot):
    bot.add_cog(Program(bot))