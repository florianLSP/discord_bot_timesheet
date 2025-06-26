import asyncio, time
from datetime import timedelta
from dataclasses import dataclass
from typing import Optional
from numpy import random

bot_commands = [
    {"name": "start", "description": "Permet de démarrer une session de travail"},
    {"name": "game1", "description": "Jeu - Pierre Feuille Ciseau"},
    {"name": "ping", "description": "Le bot répondra pong"},
]


@dataclass
class UserSession:
    start_time: float
    end_time: Optional[float] = None
    pause_start: Optional[float] = 0.0
    break_time: float = 0.0
    active: bool = False
    category: str = "Session de travail"


user_sessions = {}


def register_commands(bot, commands):
    @bot.command()
    async def ping(ctx):
        await ctx.send("pong")

    @bot.command()
    async def helpme(ctx):
        header = "**Liste des commandes disponibles :**\n"

        command_list = ""
        for bot_command in bot_commands:
            command_list += (
                f"`!{bot_command['name']}`: *{bot_command['description']}*\n"
            )

        message = header + command_list

        await ctx.send(message)

    @bot.command()
    async def start(ctx):
        await ctx.send("dis moi sur quoi tu veux bosser")
        user_id = ctx.author.id

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for("message", timeout=15.0, check=check)
            category = msg.content
        except asyncio.TimeoutError:
            category = "Session de travail"

        await ctx.send(f"Catégorie définie: {category}")

        user_sessions[user_id] = UserSession(
            start_time=time.time(), active=True, category=category
        )
        print(user_sessions[user_id])

        await ctx.send(
            f"{ctx.author.mention} → Timer démarré ! Tape `!stop` quand tu as fini."
        )

    @bot.command()
    async def stop(ctx):
        user_id = ctx.author.id

        if user_id not in user_sessions:
            await ctx.send("Aucune session en cours pour toi.")
            return

        user_session = user_sessions[user_id]
        user_session.end_time = time.time()

        if user_session.pause_start:
            user_session.break_time += user_session.end_time - user_session.pause_start

        user_session.active = False

        total_time = (
            user_session.end_time - user_session.start_time - user_session.break_time
        )
        formatted = str(timedelta(seconds=int(total_time)))

        await ctx.send(f"{ctx.author.mention} → Temps écoulé : **{formatted}**")

    @bot.command()
    async def pause(ctx):
        user_id = ctx.author.id

        if user_id not in user_sessions:
            await ctx.send("Aucune session en cours pour toi.")
            return

        user_session = user_sessions[user_id]
        if user_session.pause_start:
            await ctx.send("Tu es déjà en pause.")
            return

        user_session.break_time = time.time()
        await ctx.send("Ok, pause activée. Reviens avec `!resume`.")

    @bot.command()
    async def resume(ctx):
        user_id = ctx.author.id

        if user_id not in user_sessions:
            await ctx.send("Aucune session en cours pour toi.")
            return

        user_session = user_sessions[user_id]
        if not user_session.break_time:
            await ctx.send("Tu n'es pas en pause.")
            return

        pause_duration = time.time() - float(user_session.pause_start)
        user_session.break_time += pause_duration
        user_session.pause_start = 0.0

        await ctx.send(
            f"On y retourne ! Pause de {int(pause_duration)} secondes ajoutée."
        )

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int = 99):
        await ctx.channel.purge(limit=amount + 1)
        confirm = await ctx.send(f"🧹 {amount} messages supprimés.")
        await asyncio.sleep(3)
        await confirm.delete()
