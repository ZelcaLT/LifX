import datetime
import os 
import aiofiles
import pickle
import nextcord
import sqlite3
import aiosqlite
import urllib
import random
from nextcord.ext import ipc, commands
from nextcord.ext.commands.cooldowns import BucketType





def get_random_color():
    return random.choice([0x4287f5, 0xf54242, 0xf5f242])

def open_account(user: nextcord.Member):
    db = sqlite3.connect('data/bank.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if result:
        return
    if not result:
        sql = "INSERT INTO main(member_id, wallet, bank) VALUES(?,?,?)"
        val = (user.id, 500, 0)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

def check_bal_greater_than(user: nextcord.Member, amount: int):
    db = sqlite3.connect('data/bank.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if result[1] >= amount:
        return True
    return False

def add_bal(user: nextcord.Member, amount: int):
    db = sqlite3.connect('data/bank.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET wallet = ? WHERE member_id = ?"
    val = (result[1] + amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

def remove_bal(user: nextcord.Member, amount: int):
    db = sqlite3.connect('data/bank.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET wallet = ? WHERE member_id = ?"
    val = (result[1] - amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close() 

def remove_bank(user: nextcord.Member, amount: int):
    db = sqlite3.connect('data/bank.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET bank = ? WHERE member_id = ?"
    val = (result[1] - amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close() 


class Economy(commands.Cog, name="💲Economy"):
    """An economy system in the bot"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")
        
    @commands.command()
    @commands.is_owner()
    async def givebal(self, ctx, member: nextcord.Member, amount: int):
        add_bal(member, amount)
        await ctx.reply(f"added {amount} coins to {member.mention}")

    @commands.command(name="bal", aliases=['balance'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def balance(self, ctx, member: nextcord.Member=None):
        if member == None:
            member = ctx.author
        open_account(member)

        db = sqlite3.connect('data/bank.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE member_id = {member.id}")
        result = cursor.fetchone()

        embed = nextcord.Embed(color=get_random_color(), timestamp=ctx.message.created_at)
        embed.set_author(name=f"{member.name}'s Balance", icon_url=member.avatar.url)
        embed.add_field(name="Wallet", value=f"{result[1]} <a:lifx_coin:929818468667252797>")
        embed.add_field(name="Bank", value=f"{result[2]} <a:lifx_coin:929818468667252797>")
        embed.set_footer(text=f"Requested by {ctx.author}")

        await ctx.send(embed=embed)
        
    @commands.group(name="buy", invoke_without_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def buy(self, ctx): 
        pass

    @buy.command(name="food")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def food(self, ctx):
        amount = random.randrange(1, 7)
        possibility = random.randint(1, 25)
        if possibility == 6:
            return await ctx.reply(f"Somebody thought you were homeless while eating and gave you the money back!") 
        
        if possibility == 1: 
            amount = random.randint(7, 10)
            remove_bal(ctx.author, amount)
            return await ctx.reply(f"You paid {amount} <a:lifx_coin:929818468667252797> for some soup")
        
        remove_bal(ctx.author, amount)
        await ctx.reply(f"You paid {amount} <a:lifx_coin:929818468667252797> for a loaf of 🍞")
        
    @buy.command(name="drink")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def drink(self, ctx):
        amount = random.randrange(1, 7)
        possibility = random.randint(1, 25)
        
        if possibility == 1: 
            amount = random.randrange(1, 2)
            remove_bal(ctx.author, amount)
            return await ctx.reply(f"You paid {amount} <a:lifx_coin:929818468667252797> for 🍼")
        
        remove_bal(ctx.author, amount)
        await ctx.reply(f"You paid {amount} <a:lifx_coin:929818468667252797> for a 🍺")
        
        
        
    @commands.command(name="beg")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def beg(self, ctx):
        possibility = random.randint(1, 100)
        if possibility == 3:
            return await ctx.send(
                "You begged for coins but recieved a 🩴 instead"
            )
        if possibility == 1: 
            await ctx.reply(f"OMG! MRBEAST GAVE YOU **2,000,000** <a:lifx_coin:929818468667252797>\nYOU ARE RICH!")
            add_bal(ctx.author, 2000000)
            return

        amount = random.randrange(60, 200)

        outcomes = [
            f"You got **{amount}** <a:lifx_coin:929818468667252797>",
            f"Batman gave you **{amount}** <a:lifx_coin:929818468667252797>",
            f"You begged your mom for **{amount}** <a:lifx_coin:929818468667252797>",
            f"John Cena gave you **{amount}** <a:lifx_coin:929818468667252797>",
            f"The Rock gave you **{amount}** <a:lifx_coin:929818468667252797>",
            f"I gave you **{amount}** <a:lifx_coin:929818468667252797>",
            f"The developers gave you **{amount}** <a:lifx_coin:929818468667252797>",
            f"Your computer gave you **{amount}** <a:lifx_coin:929818468667252797>",
            f"You begged your dad for **{amount}** <a:lifx_coin:929818468667252797>",
        ]

        add_bal(ctx.author, amount)
        await ctx.send(random.choice(outcomes))
        
        
    @commands.command(name="removebal")
    @commands.is_owner()
    async def rev(self, ctx, member: nextcord.Member, amount:int): 
        remove_bal(member, amount)
        await ctx.reply(f"added {amount} coins to {member.mention}")
    
    @commands.command(name="dep", aliases=['deposit'])
    @commands.cooldown(1, 3, BucketType.user)
    async def dep(self, ctx, amount):
        db = sqlite3.connect('data/bank.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        if result[1] == 0:
            return await ctx.send(
                "You have 0 coins in your wallet :|"
            )
        done = False
        if amount == "all" or amount == "max":
            sql = "UPDATE main SET bank = ? WHERE member_id = ?"
            val = (result[2] + result[1], ctx.author.id)
            await ctx.send(f"Successfully deposited **{result[1]}** <a:lifx_coin:929818468667252797>")
            remove_bal(ctx.author, result[1])  
            done = True
        if not done:
            try:
                amount = int(amount)
            except ValueError:
                return await ctx.send(
                    "Only `integers | max | all` will be excepted as the amount"
                )
            if result[1] < amount:
                return await ctx.send(
                    f"You cannot deposit more than **{result[1]}** <a:lifx_coin:929818468667252797>"
                )
                

            sql = "UPDATE main SET bank = ? WHERE member_id = ?"
            val = (result[2] + amount, ctx.author.id)
            await ctx.send(
                f"Successfully deposited **{amount}** <a:lifx_coin:929818468667252797>"
            )
            remove_bal(ctx.author, amount)

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.command(name='gamble')
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def gamble(self, ctx, amount):
        try:
            amount = int(amount)
        except ValueError:
            self.bot.get_command("gamble").reset_cooldown(ctx)
            return await ctx.send(
                "You have to give an integer small brain"
            )

        if amount < 50:
            self.bot.get_command("gamble").reset_cooldown(ctx)
            return await ctx.send(
                "At least gamble 50 coins ._."
            )

        result = check_bal_greater_than(user=ctx.author, amount=amount)
        if result == False:
            self.bot.get_command("gamble").reset_cooldown(ctx)
            return await ctx.send(
                "Your amount cannot be greater than your balance :|"
            )

        chance = random.randint(1, 4)
        if chance != 3:
            remove_bal(ctx.author, amount)
            return await ctx.send(
                "You lost the bet!"
            )
        multiplier = random.choice([2, 2.25, 2.5, 1.25, 1.5, 1.75])
        total_wallet = int(amount * multiplier)
        add_bal(ctx.author, total_wallet)
        await ctx.send(f"You won {total_wallet} <a:lifx_coin:929818468667252797>!")

    @commands.command(name="with", aliases=['withdraw'])
    async def withdraw(self, ctx, amount: str):
        open_account(user=ctx.author)
        db = sqlite3.connect('data/bank.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()
        if result[2] == 0:
            return await ctx.send(
                "You dont have any balance in your bank :|"
            )
        done = False
        if amount == "max" or amount == "all":
            sql = "UPDATE main SET bank = ? WHERE member_id = ?"
            val = (0, ctx.author.id)
            add_bal(ctx.author, result[2])
            await ctx.send(
                f"You successfully deposited **{result[2]}** <a:lifx_coin:929818468667252797> to your bank!"
            )
            done = True
        
        if not done:
            try:
                amount = int(amount)
            except ValueError:
                return await ctx.send(
                    "Only `integers | max | all` will be accepted"
                )

            if amount >= result[2]:
                sql = "UPDATE main SET bank = ? WHERE member_id = ?"
                val = (0, ctx.author.id)
                add_bal(ctx.author, result[2])
                await ctx.send(
                    f"You successfully deposited **{result[2]}** <a:lifx_coin:929818468667252797> to your bank!"
                )
            else:
                sql = "UPDATE main SET bank = ? WHERE member_id = ?"
                val = (result[2] - amount, ctx.author.id)
                add_bal(ctx.author, amount)
                await ctx.send(
                    f"You successfully deposited **{amount}** <a:lifx_coin:929818468667252797> to your bank!"
                )
        
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.command(name='work')
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        open_account(user=ctx.author)
        chance = [1, 4]
        if chance == 2:
            return await ctx.reply(
                "You were lazy and got fired from your job!"
            )

        amount = random.randrange(400, 600)
        outcomes = [
            f"You worked in your office for **{amount}** <a:lifx_coin:929818468667252797>",
            f"Your boss was frustrated but you worked for him and got **{amount}** <a:lifx_coin:929818468667252797>",
            f"You begged your boss for **{amount}** <a:lifx_coin:929818468667252797>",
            f"You killed your boss and got **{amount}** <a:lifx_coin:929818468667252797> from his wallet",
            f"You got a promotion! You earned **{amount}** <a:lifx_coin:929818468667252797> today :D"
        ]

        await ctx.send(random.choice(outcomes))
        add_bal(ctx.author, amount)
    



def setup(bot):
    bot.add_cog(Economy(bot))