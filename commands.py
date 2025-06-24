import asyncio

bot_commands = [
    {"name": "start", "description": "Permet de démarrer une session de travail"},
    {"name": "ping", "description": "Le bot répondra pong"},
]


def register_commands(bot):
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
