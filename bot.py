import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
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

@bot.tree.command(name="ssh", description="SSH Informations")
async def ssh(interaction: discord.Interaction):
    await interaction.response.send_message("SSH Information: \n- Host: example.com\n- Port: 22\n- User: user")

@bot.tree.command(name="embed", description="Embed Example")
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(title="Example Embed", description="This is an example of an embed message.", color=discord.Color.blue())
    embed.add_field(name="Field 1", value="This is the first field.", inline=False)
    embed.add_field(name="Field 2", value="This is the second field.", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(os.getenv('DISCORD_TOKEN'))
