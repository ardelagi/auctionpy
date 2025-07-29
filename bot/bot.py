import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils.auction_manager import AuctionManager

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
auction_manager = AuctionManager(bot)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} siap!')
    await bot.load_extension('commands.startauction')
    await bot.load_extension('commands.stopauction')
    await bot.load_extension('commands.setauctiontimer')
    
    synced = await bot.tree.sync()
    print(f"Command tersinkronisasi: {len(synced)}")
    
    await bot.load_extension('commands.startauction')
    

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await auction_manager.process_bid(message)
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_TOKEN'))