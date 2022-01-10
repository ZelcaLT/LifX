import datetime
import urllib
import os 
import aiofiles
import nextcord
import aiosqlite
import urllib
import json
import asyncio
import asyncpraw
import random
from nextcord import channel
from nextcord.components import Button
from nextcord.ext import ipc, commands
from nextcord.ext.commands.cooldowns import BucketType
from nextcord.ext.commands.errors import MissingRequiredArgument
from nextcord.types.components import ButtonStyle

reddit = asyncpraw.Reddit(client_id = "id",
                          client_secret = "secret",
                          username = "user",
                          password = "password",
                          user_agent = "agent",
                          check_for_async = False)



class Fun(commands.Cog, name="😂Fun"):

    def __init__(self, bot):
        self.bot = bot

        
    """Cogs for memes and jokes"""

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")


    @commands.command(name="aww", description="Shows some cute moments from reddit. (note: this command sometimes takes a while to load; this is as the bot needs to go through hundreds of posts.)", aliases=["cute"])
    @commands.cooldown(1, 5, BucketType.member)
    async def aww(self, ctx):
        subreddit = await reddit.subreddit("aww")
        all_subs = []
        async for submission in subreddit.top(limit=250):
            all_subs.append(submission)

        random_sub = random.choice(all_subs)
        name = random_sub.title
        url = random_sub.url
        author = random_sub.author


        e = nextcord.Embed(title=name, description=f"From **u/{author}** in subreddit **aww**")
        await ctx.reply(embed=e)
        await ctx.send(url)

    @commands.command(name="dogs", description="Doggos!", aliases=["doggos"])
    @commands.cooldown(1, 5, BucketType.member)
    async def dogs(self, ctx):
        subreddit = await reddit.subreddit("lookatmydog")
        all_subs = []
        async for submission in subreddit.hot(limit=150):
            all_subs.append(submission)

        random_sub = random.choice(all_subs)
        name = random_sub.title
        url = random_sub.url

        e = nextcord.Embed(title=name)
        await ctx.reply(embed=e)
        await ctx.send(url)






    @commands.command(name="meme", description="A meme command that generates a meme from Reddit.")
    async def meme(self, ctx):
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
        await ctx.send("heres ya meme u granny")
        await ctx.send(embed=embed)

    @commands.command(name="say", description="Say something as the bot.")
    async def say(self, ctx, message):
        await ctx.message.delete()
        await ctx.send(message + "\n\n\- {}".format(ctx.author.display_name))

    @commands.command(name="hack", description="hackle into some1s account (tottaly reall)")
    async def hack(self, ctx, target: nextcord.Member):
        author = ctx.author
        email = [
            f"{target.display_name}018011@hotmail.com".strip(),
            f"{target.display_name}326981@gmail.com".strip(),
            f"{target.display_name}15216@disorcd.gov".strip(),
            f"{target.display_name}881451@nothing.edu".strip(),
            f"{target.display_name}69420@memez.org".strip(),
            f"{target.display_name}001741@icloud.com".strip()

        ]

        password = [
            "ilovemymother@16",
            "iDontLeaveMyHouse999+",
            "password",
            "p455w0rd",
            "iamsecure123",
            "hJAHD898988",
            "beautifulSunset663",
            "iAmVeganandOnADiet1157",
            "discordIsMyHome8UODG/AF",
            "hUHDpoj98//f@~#"
        ]

        ip = [
            "125.153.000.1",
            "129.166.255.255",
            "255.255.255.256",
            "156.514.888.014",
            "127.888.554.199",
            "130.188.216.65",
            "241.3.70.19",
            "184.98.207.79",
            "38.148.141.105",
            "247.50.249.154",
            "198.214.99.241",
            "175.107.85.251",
            "88.137.120.67",
            "40.77.200.5",
            "203.188.118.141",
            "52.27.103.45",
            "232.212.92.144",
            "64.254.124.238",
            "118.54.121.235",
            "133.15.10.63",
            "183.49.43.31",
            "84.214.147.156",
            "229.69.88.146",
            "143.14.251.185",
            "17.15.115.251",
            "145.234.206.43",
            "237.178.54.120",
            "228.174.51.38",
            "80.24.92.210",
            "127.72.58.171",
            "159.136.46.67",
            "13.142.172.14",
            "32.213.26.134",
            "10.77.121.165",
            "184.134.137.94",
            "77.221.23.223",
            "36.143.70.56",
            "47.183.204.2",
            "175.161.147.193",
            "102.225.224.146",
            "228.185.114.82",
            "177.151.137.155",
            "43.6.157.86",
            "55.160.49.189",
            "54.63.85.175",
            "54.137.26.99",
            "184.34.182.37",
            "204.137.37.51",
            "195.127.37.248",
            "153.226.110.190",
            "74.204.144.216",
            "60.9.245.144",
            "118.225.178.140",
            "227.135.58.55",
            "42.3.113.107"
        ]

        a = await ctx.send(f"Hacking into **{target.display_name}**'s account now...")
        await asyncio.sleep(1.513)
        a1 = ("Getting discord login (2fa disabled)")
        a2 = (f"Login found!\n**Email:**\n`{random.choice(email)}`\n**Password:**\n`{random.choice(password)}`")
        a3 = ("Finding IP Address... (geolocation enabled)")
        a4 = (f"IP found!\n`{random.choice(ip)}`")
        await asyncio.sleep(2.001)
        await a.edit(a1)
        await asyncio.sleep(3)
        await a.edit(a2)
        await asyncio.sleep(3)
        await a.edit(a3)
        await asyncio.sleep(3)
        await a.edit(a4)








def setup(bot):
    bot.add_cog(Fun(bot))
