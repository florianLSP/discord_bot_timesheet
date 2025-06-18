import os
from dotenv import load_dotenv
import discord
from discord.ext import commands


load_dotenv()
token = os.getenv("DISCORD_TOKEN")

print(f"Token lu : {token}") 

intents = discord.Intents.default()
intents.message_content = True 
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents = intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user.name}")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


bot.run(token)
