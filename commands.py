import asyncio, time
from datetime import timedelta

bot_commands = [
    {"name": "start", "description": "Permet de démarrer une session de travail"},
    {"name": "ping", "description": "Le bot répondra pong"},
]

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

        # Fonction qui prend en compte que le message de l'utilisateur qui a
        # exécuté la commande dans le salon.
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            # timer de 10 secondes pour récupérer la catégorie
            msg = await bot.wait_for("message", timeout=15.0, check=check)
            category = msg.content
        except asyncio.TimeoutError:
            category = "Session de travail"

        await ctx.send(f"Catégorie définie: {category}")
        global start_timer
        start_timer = time.time()
        user_sessions[user_id] = start_timer
        await ctx.send(
            f"{ctx.author.mention} → Timer démarré ! Tape `!stop` quand tu as fini."
        )

    @bot.command()
    async def stop(ctx):
        user_id = ctx.author.id

        if user_id not in user_sessions:
            await ctx.send("Aucune session en cours pour toi.")
            return

        global end_timer
        end_timer = int(time.time())
        timer = end_timer - user_sessions[user_id]

        formatted = str(timedelta(seconds=int(timer)))
        await ctx.send(f"{ctx.author.mention} → Temps écoulé : **{formatted}** ⏱️")

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int = 10):
        await ctx.channel.purge(limit=amount + 1)
        confirm = await ctx.send(f"🧹 {amount} messages supprimés.")
        await asyncio.sleep(3)
        await confirm.delete()
