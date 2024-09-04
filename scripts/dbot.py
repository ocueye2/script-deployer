
import discord
from discord import app_commands
from discord.ext import commands
from mcrcon import MCRcon

# Set up the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Minecraft RCON credentials
RCON_HOST = '192.168.1.130'
RCON_PORT = 25575  # default RCON port
RCON_PASSWORD = 'admin'

# Command to whitelist a player
@bot.tree.command(name='whitelist', description='Whitelist a player on the Minecraft server')
async def whitelist(interaction: discord.Interaction, username: str):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, RCON_PORT) as mcr:
            response = mcr.command(f'whitelist add {username}')
            await interaction.response.send_message(f'Player {username} has been whitelisted.')
    except Exception as e:
        await interaction.response.send_message(f'Failed to whitelist {username}. Error: {e}')

@bot.tree.command(name='info', description='list server info')
async def whitelist(interaction: discord.Interaction):
    await interaction.response.send_message(f'the server id is mc.carsonmayn.com \nget the mods at https://pub.carsonmayn.com/mods/ .thank you for useing the bot')

@bot.tree.command(name='drcon', description='admin only')
async def whitelist(interaction: discord.Interaction, rcon: str):
    print(str(interaction.user))
    if str(interaction.user) == "ocueye":
        try:
            with MCRcon(RCON_HOST, RCON_PASSWORD, RCON_PORT) as mcr:
                response = mcr.command(rcon)
                await interaction.response.send_message(response)
        except Exception as e:
            await interaction.response.send_message(f'Error running {rcon}. \nError: {e}')

    else:
        await interaction.response.send_message(f'Error running {rcon}. \nError: You do not have the priviage to use this command')

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')

# Run the bot
bot.run('MTE1NDgzODE4Mjc4NTk5NDc4NQ.Gz1ZHo.CAXdgHPJ6CgnQEcAr6xXjUIj2DMfJkCLFu_Uxo')
