import os
import json
import asyncio
import time
import uuid
from datetime import timedelta, datetime
from dataclasses import dataclass
from typing import Optional

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


log_state = {"count": 0}


def print_logs(id_user, username, command, user_session=None):
    log_state["count"] += 1
    print("\n****************************************************************\n")
    print(f"log n°{log_state['count']}")
    print(f"id: {id_user}")
    print(f"nom: {username}")
    print(f"commande: {command}")
    print(f"user_session: {user_session}")
    print("\n****************************************************************\n")


def create_user_file(user_id, username):
    filename = f"users/{username}_{user_id}.json"

    if not os.path.exists("users"):
        os.makedirs("users")

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f, indent=4)
            print(f"Fichier créé pour {username}")
    else:
        print(f"Pas de création de fichier pour {username} car déjà existant.")


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

        print_logs(
            ctx.author.id,
            ctx.author.name + " (@" + ctx.author.display_name + ")",
            "!helpme",
        )
        await ctx.send(message)

    @bot.command()
    async def start(ctx):
        user_id = ctx.author.id
        username = ctx.author.name
        filename = f"users/{username}_{user_id}.json"
        is_existing_date = False

        create_user_file(user_id, username)

        await ctx.send("Dis-moi sur quoi tu veux bosser (tu as 15 secondes) 🧠")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for("message", timeout=15.0, check=check)
            category = msg.content.strip()
        except asyncio.TimeoutError:
            category = "Session de travail"

        await ctx.send(f"📌 Catégorie définie : `{category}`")

        with open(filename, "r") as f:
            user_data = json.load(f)

        new_session_id = str(uuid.uuid4())
        today = datetime.now().strftime("%d/%m/%Y")

        new_session = {
            "id_session": new_session_id,
            "category": category,
            "description": "test description",
            "start_time": time.time(),
            "end_time": None,
            "pause_start": None,
            "break_time": 0,
        }

        for entry in user_data:
            if entry["date"] == today:
                entry["sessions"].append(new_session)
                is_existing_date = True
                break

        if not is_existing_date:
            user_data.append({"date": today, "sessions": [new_session]})

        with open(filename, "w") as f:
            json.dump(user_data, f, indent=4)

        print_logs(
            user_id, f"{username} (@{ctx.author.display_name})", "!start", new_session
        )

        await ctx.send(
            f"{ctx.author.mention} → ✅ Timer démarré ! Tape `!stop` quand tu as fini."
        )

    @bot.command()
    async def stop(ctx):
        user_id = ctx.author.id
        username = ctx.author.name
        filename = f"users/{username}_{user_id}.json"
        today = datetime.now().strftime("%d/%m/%Y")

        if not os.path.exists(filename):
            await ctx.send("Aucune session trouvée pour toi.")
            return

        with open(filename, "r") as f:
            user_data = json.load(f)

        session_found = False
        for entry in user_data:
            if entry["date"] == today:
                for session in reversed(entry["sessions"]):
                    if session["end_time"] is None:
                        end_time = time.time()
                        session["end_time"] = end_time

                        if session["pause_start"]:
                            session["break_time"] += end_time - session["pause_start"]
                            session["pause_start"] = None

                        total_time = (
                            session["end_time"]
                            - session["start_time"]
                            - session["break_time"]
                        )
                        formatted = str(timedelta(seconds=int(total_time)))

                        with open(filename, "w") as f:
                            json.dump(user_data, f, indent=4)

                        print_logs(
                            user_id,
                            f"{username} (@{ctx.author.display_name})",
                            "!stop",
                            session,
                        )
                        await ctx.send(
                            f"{ctx.author.mention} → Temps écoulé : **{formatted}** ⏱️"
                        )
                        session_found = True
                        break
                break
        if not session_found:
            await ctx.send("Aucune session en cours trouvée pour aujourd'hui")


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

        user_session.pause_start = time.time()

        print_logs(
            ctx.author.id,
            ctx.author.name + " (@" + ctx.author.display_name + ")",
            "!pause",
            user_sessions[user_id],
        )
        await ctx.send("Ok, pause activée. Reviens avec `!resume`.")

    @bot.command()
    async def resume(ctx):
        user_id = ctx.author.id

        if user_id not in user_sessions:
            await ctx.send("Aucune session en cours pour toi.")
            return

        user_session = user_sessions[user_id]
        if not user_session.pause_start:
            await ctx.send("Tu n'es pas en pause.")
            return

        pause_duration = time.time() - float(user_session.pause_start)
        user_session.break_time += pause_duration
        user_session.pause_start = 0.0
        formatted = str(timedelta(seconds=int(pause_duration)))

        print_logs(
            ctx.author.id,
            ctx.author.name + " (@" + ctx.author.display_name + ")",
            "!resume",
            user_sessions[user_id],
        )
        await ctx.send(f"On y retourne ! Pause de {formatted} secondes ajoutée.")

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int = 99):
        print_logs(
            ctx.author.id,
            ctx.author.name + " (@" + ctx.author.display_name + ")",
            "!clear",
        )
        await ctx.channel.purge(limit=amount + 1)
        confirm = await ctx.send(f"🧹 {amount} messages supprimés.")
        await asyncio.sleep(3)
        await confirm.delete()
