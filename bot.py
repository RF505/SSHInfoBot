import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import subprocess
load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        sync = await bot.tree.sync()
        print(f'Synced {len(sync)} commands.')
    except Exception as e:
        print(e)

@bot.event
async def on_message(message: discord):
    if message.content == '!ping':
        await message.channel.send('Pong!')

#@bot.tree.command(name="ssh", description="SSH Informations")
#async def ssh(interaction: discord.Interaction):
#    await interaction.response.send_message("SSH Information: \n- Host: example.com\n- Port: 22\n- User: user")



class SSHView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Afficher plus d'infos", style=discord.ButtonStyle.primary, custom_id="ssh_more_info")
    async def more_info_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            result = subprocess.check_output(
                ["sudo", "fail2ban-client", "status", "sshd"],
                stderr=subprocess.STDOUT,
                text=True
            )

            banned_ips = "Aucune IP bannie."
            for line in result.splitlines():
                if "Banned IP list" in line:
                    banned_ips = line.split(":", 1)[1].strip()
                    break

            bannedipembed = discord.Embed(
            title="SSH Détails",
            description="Voici les IP actuellement bannies par Fail2Ban :",
            color=discord.Color.red()
            )

            # Formatage des IPs en bloc de code avec retour à la ligne
            ips_formattees = "```\n" + "\n".join(banned_ips.split()) + "\n```"

            bannedipembed.add_field(name="IP bannies", value=ips_formattees if banned_ips else "Aucune", inline=False)

            await interaction.response.send_message(embed=bannedipembed, ephemeral=True)

        except subprocess.CalledProcessError as e:
            await interaction.response.send_message(
                f"Erreur lors de la récupération des IP bannies :\n```\n{e.output}\n```",
                ephemeral=True
            )


@bot.tree.command(name="ssh", description="SSH Informations")
async def ssh(interaction: discord.Interaction):
    embed1 = discord.Embed(
        title="SSH Exemple",
        description="Ceci est un embed public avec des infos de base.",
        color=discord.Color.blue()
    )
    embed1.add_field(name="Info", value="Clique sur le bouton pour plus de détails.", inline=False)

    view = SSHView()
    await interaction.response.send_message(embed=embed1, view=view)

bot.run(os.getenv('DISCORD_TOKEN'))
