def register_events(bot, channel_id):
    @bot.event
    async def on_ready():
        print(f"Connecté en tant que {bot.user.name}")

    @bot.event
    async def on_voice_state_update(member, before, after):
        print(
            f"\n****************************************************************\n Utilisateur : {member.name}(@{member.display_name}) \n Channel précédent: {before.channel} \n Channel suivant: {after.channel} \n****************************************************************\n"
        )

        # Vérification que l'user n'est pas parti et qu'il a bien changé de channel.
        if after.channel is not None and before.channel != after.channel:
            if after.channel.id == channel_id:
                # Récupère le salon de l'utilisateur Discord dans le serveur à partir de son ID
                text_channel = member.guild.get_channel(channel_id)
                if text_channel:
                    await text_channel.send(
                        f"Yooo!! {member.mention} est la pour bosser ! \n Fais moi signe quand tu es prêt à commencer ! (`!start` ou `!helpme` pour afficher les commandes)"
                    )
