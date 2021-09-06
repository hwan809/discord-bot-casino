import discord
from discord.ext import commands
from modules.helpers import *

TOKEN = 'NzUxNjQ0NzU0NjAwNzg4MDY4.X1MFug.cMPkipIC0vJh6pTi9KRyNvD6Pno'

client = commands.Bot(
    command_prefix=PREFIX,
    owner_ids=OWNER_IDS,
    intents=discord.Intents.all()
)
client.remove_command('help')

for filename in os.listdir(COG_FOLDER):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
