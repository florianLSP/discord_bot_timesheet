import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio


load_dotenv()
token = os.getenv("DISCORD_TOKEN")
channel_id = int(os.getenv("CHANNEL_1_ID"))


intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True  # utile plus tard
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user.name}")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.event
async def on_voice_state_update(member, before, after):
    print(
        f"******************\n Channel précédent: {before.channel} \n Channel suivant: {after.channel} \n******************"
    )

    # Vérification que l'user n'est pas parti et qu'il a bien changé de channel.
    if after.channel is not None and before.channel != after.channel:
        if after.channel.id == channel_id:
            # Récupère le salon de l'utilisateur Discord dans le serveur à partir de son ID
            text_channel = member.guild.get_channel(channel_id)
            if text_channel:
                await text_channel.send(
                    f"Yooo!! {member.display_name} est la pour bosser !"
                )
                await asyncio.sleep(1)
                await text_channel.send(
                    f"Fais moi signe quand tu es prêt à commencer ! (!start)"
                )


bot.run(token)
