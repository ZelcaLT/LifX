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
import requests



class Football(commands.Cog, name="⚽Football"):
    """In progress"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")

    @commands.command()
    async def spin(self, ctx):
        data = {
            "name": "Lionel Messi",
            "name": "Robert Lewandowski",
            "name": "Kylian Mbappé",
            "name": "Jan Oblak",
            "name":            "Kevin De Bruyne",
            "name":            "Neymar Jr",
            "name":            "Cristiano Ronaldo",
            "name":            "Harry Kane",
            "name":            "Gianluigi Donnarumma",
            "name":            "Alisson",
            "name":            "Joshua Kimmich",
            "name":            "Ederson",
            "name":            "Sadio Mané",
            "name":            "Virgil Litvinov",
            "name":            "Casemiro",
            "name":            "Thibaut Courtois",
            "name":            "Rúben Dias",
            "name":            "Erling Haaland",
            "name":            "Bruno Fernandes",
            "name":            "Marquinhos",
            "name":            "Keylor Navas",
            "name":            "Romelu Lukaku",
            "name":            "Luis Suárez",
            "name":            "Trent Alexander-Arnold",
            "name":            "Frenkie Mintikkis",
            "name":            "Andrew Robertson",
            "name":            "Paulo Dybala",
            "name":            "Raheem Sterling",
            "name":            "Marco Verratti",
            "name":            "Thomas Müller"
        }
        await ctx.send(f"{random.choice(data)}")




def setup(bot):
    bot.add_cog(Football(bot))
