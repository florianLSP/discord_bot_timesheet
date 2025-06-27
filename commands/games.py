import asyncio
from numpy import random


def register_games(bot):
    @bot.command()
    async def game1(ctx):
        await ctx.send(
            f"Ok {ctx.author.mention}, tu veux jouer au pierre feuille ciseau ? (o = oui, n = non)"
        )

        try:
            msg = await bot.wait_for("message", timeout=15.0)
            choice = msg.content
        except asyncio.TimeoutError:
            choice = "Ok on jouera plus tard..."

        if choice == "o":
            await ctx.send("Début de la game :\n p = pierre\n f = feuille\n c = ciseau")
            countdown = await ctx.send("Début de la partie dans ... 3")
            await asyncio.sleep(1)
            await countdown.edit(content="Début de la partie dans ... 2")
            await asyncio.sleep(1)
            await countdown.edit(content="Début de la partie dans ... 1")
            await asyncio.sleep(1)
            await countdown.edit(content="Début de la partie dans ... 0")

            try:
                msg2 = await bot.wait_for("message", timeout=5)
                user_choice = msg2.content
                print(user_choice)
            except asyncio.TimeoutError:
                user_choice = "T'as pas compris, tu dois choisir entre p = pierre, f = feuille, c = ciseau"

            bot_choice = random.choice(["p", "f", "c"])

            if user_choice == "p":
                if bot_choice == "c":
                    await ctx.send("✂️ \n Tu as gagné!!!")
                elif bot_choice == "f":
                    await ctx.send("🍁 \n Tu as perdu...")
                else:
                    await ctx.send("🗿 \n Égalité bravo à vous deux !")

            if user_choice == "f":
                if bot_choice == "c":
                    await ctx.send("✂️ \n Tu as perdu...")
                elif bot_choice == "f":
                    await ctx.send("🍁 \n Égalité bravo à vous deux !")
                else:
                    await ctx.send("🗿 \n Tu as gagné!!!")

            if user_choice == "c":
                if bot_choice == "c":
                    await ctx.send("✂️ \n Égalité bravo à vous deux !")
                elif bot_choice == "f":
                    await ctx.send("🍁 \n Tu as gagné!!!")
                else:
                    await ctx.send("🗿 \n Tu as perdu...")

        else:
            await ctx.send("Ok on jouera plus tard...")
