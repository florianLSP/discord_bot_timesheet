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
bot_commands = [
    {"name": "start", "description": "Permet de démarrer une session de travail"},
    {"name": "ping", "description": "Le bot répondra pong"},
]


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user.name}")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def helpme(ctx):
    header = "**Liste des commandes disponibles :**\n"

    command_list = ""
    for bot_command in bot_commands:
        command_list += f"`!{bot_command['name']}`: *{bot_command['description']}*\n"

    message = header + command_list

    await ctx.send(message)


@bot.command()
async def start(ctx):
    await ctx.send("dis moi sur quoi tu veux bosser")

    # Fonction qui prend en compte que le message de l'utilisateur qui a
    # exécuté la commande dans le salon.
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # timer de 10 secondes pour récupérer la catégorie
        msg = await bot.wait_for("message", timeout=10.0, check=check)
        category = msg.content
    except asyncio.TimeoutError:
        category = "Session de travail"

    await ctx.send(f"Catégorie définie: {category}")


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
                    f"Yooo!! {member.mention} est la pour bosser ! \n Fais moi signe quand tu es prêt à commencer ! (`!start` ou `!help` pour afficher les commandes)"
                )


bot.run(token)
