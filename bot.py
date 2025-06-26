import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from commands.main_commands import register_commands
from commands.games import register_games
from events import register_events


load_dotenv()
token = os.getenv("DISCORD_TOKEN")
channel_id = int(os.getenv("CHANNEL_1_ID"))


intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True  # utile plus tard
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


register_commands(bot, commands)
register_games(bot)
register_events(bot, channel_id)


bot.run(token)
