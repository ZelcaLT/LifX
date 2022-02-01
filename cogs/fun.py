import datetime
from typing import List, Optional
import urllib
import os 
import aiofiles
import nextcord
import aiosqlite
import urllib
import akinator as ak
import json
import asyncio
import asyncpraw
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont



from nextcord import channel
from nextcord.components import Button
from nextcord.ext import ipc, commands
from nextcord.ext.commands.cooldowns import BucketType
from nextcord.ext.commands.errors import MissingRequiredArgument
from nextcord.types.components import ButtonStyle
from utils import hangman, twenty, hmgroup

reddit = asyncpraw.Reddit(client_id = "id",
                          client_secret = "secret",
                          username = "user",
                          password = "password",
                          user_agent = "agent",
                          check_for_async = False)

class TicTacToeButton(nextcord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=nextcord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = nextcord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = nextcord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(nextcord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + \
                self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

class Fun(commands.Cog, name="😂Fun"):
    """Commands for memes and jokes"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")

    @commands.command()
    async def thumbsup(self, ctx):
        channel = ctx.message.channel
        await channel.send('Send me that 👍 reaction, mate')

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('👎')
        else:
            await channel.send('👍')

    @commands.command(name="tic", description="Play a game of tic-tac-toe with yourself.")
    async def tic(self, ctx):
        await ctx.reply("Tic Tac Toe: X goes first", view=TicTacToe())

    async def getMessages(self, ctx, number: int = 1):
        if number == 0:
            return []
        toDelete = []
        async for x in ctx.channel.history(limit=number):
            toDelete.append(x)
        return toDelete

    @commands.command(name="rps", description="Play Rock Paper Scissors.",aliases=["rockpaperscissors"])
    async def rps(self, ctx):
        """Play Rock, Paper, Scissors game"""

        def check_win(p, b):
            if p == "🌑":
                return False if b == "📄" else True
            if p == "📄":
                return False if b == "✂" else True
            # p=='✂'
            return False if b == "🌑" else True

        async with ctx.typing():
            reactions = ["🌑", "📄", "✂"]
            game_message = await ctx.send(
                "**Rock Paper Scissors**\nChoose your shape:", delete_after=15.0
            )
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction, user):
            return (
                user != self.bot.user
                and user == ctx.author
                and (str(reaction.emoji) == "🌑" or "📄" or "✂")
            )

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", timeout=10.0, check=check
            )
        except asyncio.TimeoutError:
            await ctx.send("Time's Up! :stopwatch:")
        else:
            await ctx.send(
                f"**:man_in_tuxedo_tone1:\t{reaction.emoji}\n:robot:\t{bot_emoji}**"
            )
            # if conds
            if str(reaction.emoji) == bot_emoji:
                await ctx.send("**It's a Tie :ribbon:**")
            elif check_win(str(reaction.emoji), bot_emoji):
                await ctx.send("**You win :sparkles:**")
            else:
                await ctx.send("**I win :robot:**")
                


    @commands.command(aliases=["aki"])
    async def akinator(self, ctx):
        await ctx.reply("Akinator is here to guess!")

        def check(msg):
            return (
                msg.author == ctx.author
                and msg.channel == ctx.channel
                and msg.content.lower() in ["y", "n", "p", "b"]
            )

        try:
            aki = ak.Akinator()
            q = aki.start_game()
            while aki.progression <= 80:
                em = nextcord.Embed(
                    title="Answer:",
                    description=q
                )
                await ctx.send(embed=em)
                em2 = nextcord.Embed(
                    title="Answer:",
                    description="y/n/p/b"
                )

                await ctx.send("Your answer: (y/n/p/b)")
                msg = await self.bot.wait_for("message", check=check)
                if msg.content.lower() == "b":
                    try:
                        q = aki.back()
                    except ak.CantGoBackAnyFurther as e:
                        await ctx.send(e)
                        continue
                else:
                    try:
                        q = aki.answer(msg.content.lower())
                    except ak.InvalidAnswerError as e:
                        await ctx.send(e)
                        continue
            aki.win()
            em3 = nextcord.Embed(
                title=f"It's {aki.first_guess['name']} ({aki.first_guess['description']})!",
                description=f"Was I correct?\ny/n\n",
                color=nextcord.Colour.random()
            )
            em3.set_image(url=f"{aki.first_guess['absolute_picture_path']}")
            
            await ctx.send(embed=em3)
            correct = await self.bot.wait_for("message", check=check)
            if correct.content.lower() == "y":
                await ctx.send("Yay!\nPlay again with `==aki`\n")
            else:
                await ctx.send("Oh...\nPlay again with `==aki`\n")
        except Exception as e:
            await ctx.send(e)



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

    @commands.command(name="obama", description="Say something as obama.")
    async def obama(self, ctx, *, txt):
        caption = txt


        image = Image.open('obama.jpg')
        font = ImageFont.truetype("Roboto-Black.ttf", 75)



        draw2 = ImageDraw.Draw(image)

        margin = 250
        offset = 500
        for line in textwrap.wrap(caption, width=30):
            draw2.text((margin, offset), line, font=font, fill="#ffffff")
            offset += font.getsize(line)[1]

        image.save("obama2.jpg")

        await ctx.reply(file = nextcord.File("obama2.jpg"))

    @commands.command(name="hangman", description="Play a game of hangman!")
    async def hangman(self, ctx):
        """Play Hangman"""
        await hangman.play(self.bot, ctx)
        

    @commands.command()
    async def simprate(self, ctx, member: Optional[nextcord.Member], *, simpable: Optional[str],
    ):
        """Find out how much someone is simping for something."""
        member = member or ctx.author
        rate = random.choice(range(1, 100))
        if simpable:
            message = f"{member.mention} is **{rate}**% simping for {simpable} 😳"
        else:
            message = f"{member.mention} is **{rate}**% simp 😳"
        await ctx.send(
            message, allowed_mentions=nextcord.AllowedMentions(users=False)
        )

    @commands.command()
    async def clownrate(
        self, ctx, member: Optional[nextcord.Member]):
        """Reveal someone's clownery."""
        member = member or ctx.author
        rate = random.choice(range(1, 100))
        emoji = self.bot.get_emoji(758821900808880138) or "🤡"
        message = f"{member.mention} is **{rate}**% clown {emoji}"
        await ctx.send(
            message, allowed_mentions=nextcord.AllowedMentions(users=False)
        )

    @commands.command(aliases=["iq"])
    async def iqrate(self, ctx, member: Optional[nextcord.Member]):
        """100% legit IQ test."""
        member = member or ctx.author
        random.seed(member.id + self.bot.user.id)
        if await self.bot.is_owner(member):
            iq = random.randint(200, 500)
        else:
            iq = random.randint(-10, 200)
        if iq >= 160:
            emoji = self.bot.get_emoji(758821860972036106) or "🧠"
        elif iq >= 100:
            emoji = self.bot.get_emoji(758821993768026142) or "🤯"
        else:
            emoji = self.bot.get_emoji(758821971319586838) or "😔"
        await ctx.send(
            f"{member.mention} has an IQ of {iq} {emoji}",
            allowed_mentions=nextcord.AllowedMentions(users=False),
        )



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
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        e = nextcord.Embed(title=" ", description=message)
        e.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=e)

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



    @commands.command(name="2048")
    async def twenty(self, ctx):
        """Play 2048 game"""
        await twenty.play(ctx, self.bot)





def setup(bot):
    bot.add_cog(Fun(bot))
