import datetime
import os 
import aiofiles
import pickle
import nextcord
import aiosqlite
import urllib
import random
from nextcord.ext import ipc, commands
import config
from nextcord.ext.commands.cooldowns import BucketType
import math



def add(n: float, n2: float):
	return n + n2

def sub(n: float, n2: float):
	return n - n2

def rando(n: int, n2: int):
	return random.randint(n, n2)

def div(n: float, n2: float):
	return n / n2

def sqrt(n: float):
	return math.sqrt(n)

def mult(n: float, n2: float):
	return n * n2

def lthan(n: float, n2: float):
    return n < n2

def mthan(n: float, n2: float):
    return n > n2

class Calc(commands.Cog, name="➕Calculator"):
    """Calculate some things"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")

    @commands.group(invoke_without_command=True)
    async def math(self, ctx):    
        cog = Calc(self)
        await ctx.reply(f"```{[c.qualified_name for c in cog.walk_commands()]}```")

    @math.command()
    async def add(self, ctx, x: float, y: float):
        result = add(x, y)
        e = nextcord.Embed(
            title="Result",
            description=result,
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)


    @math.command()
    async def sub(self, ctx, x: float, y: float):
        result = sub(x, y)
        e = nextcord.Embed(
            title="Result",
            description=result,
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)


    @math.command()
    async def rando(self, ctx, x: int, y: int):
        result = rando(x, y)
        e = nextcord.Embed(
            title="Result",
            description=result,
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)


    @math.command()
    async def div(self, ctx, x: float, y: float):
        result = div(x, y)
        e = nextcord.Embed(
            title="Result",
            description=result,
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)

    @math.command()
    async def mult(self, ctx, x: float, y: float):
        result = mult(x, y)
        e = nextcord.Embed(
            title="Result",
            description=result,
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)

    @math.command()
    async def lthan(self, ctx, x: float, y: float):
        result = lthan(x, y)
        e = nextcord.Embed(
            title="Result",
            description=result,
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)

    @math.command()
    async def mthan(self, ctx, x: float, y: float):
        result = mthan(x, y)
        e = nextcord.Embed(
            title="Result",
            description=result,
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)


    @math.command()
    async def sqrt(self, ctx, x: float):
        result = sqrt(x)
        e = nextcord.Embed(
            title="Result",
            description=result,
            color=nextcord.Colour.random()
        )
        await ctx.reply(embed=e)




def setup(bot):
    bot.add_cog(Calc(bot))
