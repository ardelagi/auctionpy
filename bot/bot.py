import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from utils.auction_manager import AuctionManager

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
auction_manager = AuctionManager(bot)

async def load_cogs():
    await bot.load_extension('commands.startauction')
    await bot.load_extension('commands.stopauction')
    await bot.load_extension('commands.setauctiontimer')

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} ready!')
    await load_cogs()
    
    # Sync slash commands
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands.")
    
    # List registered commands
    commands_list = await bot.tree.fetch_commands()
    print("Registered commands:")
    for cmd in commands_list:
        print(f"- {cmd.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Process bids before commands
    await auction_manager.process_bid(message)
    
    # Process commands
    await bot.process_commands(message)

if __name__ == "__main__":
    asyncio.run(bot.start(os.getenv('DISCORD_TOKEN')))