import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

Conan = discord.Bot(intents=intents,
                   status = discord.Status.online,
                   debug_guilds=[os.getenv("DEBUG_GUILD")])

@Conan.event
async def on_ready():
    print(f'{Conan.user} ist online!')
    print('------' * 10)
    

def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                Conan.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print(f'Fehler beim Laden von {filename}: {e}')



if __name__ == '__main__':
    load_cogs()
    Conan.run(os.getenv('BOT_TOKEN'))