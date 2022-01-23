import nextcord as nc
from nextcord.ext import commands as cs
from nextcord import Colour, Interaction

spex = cs.Bot(command_prefix='spex ', intents=nc.Intents.all())
spex.remove_command("help")
id = 921758771158605834


@spex.event
async def on_ready():
    print("Spex is online")



@spex.command(name="ping", description="Shows the current ping of the bot")
async def ping(ctx):
    em = nc.Embed(title="Pong! 🏓", description=f"{round(spex.latency * 1000)}ms", color=Colour.random())
    await ctx.reply(embed=em)

@spex.slash_command(name="help", description="Shows help for the Spex bot.", guild_ids=[id])
async def help(interaction : Interaction):

    em = nc.Embed(title="Help",description="Prefix: `spex `\nSpex is a bot designed to help verify bots for The Coders discord server.")

    await interaction.response.send_message(embed=em)

spex.run("OTM0OTM5MDExNjE1Njg2NzU2.Ye3Xzg.C-P_rsHC9pUuqU6A7YoM4FMypWA")