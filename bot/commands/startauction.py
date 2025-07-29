import discord
from discord import app_commands
from discord.ext import commands
from utils.auction_manager import AuctionManager
from models.auction import AuctionModel
from config import ADMIN_ROLE_ID, DEFAULT_TIMER

class StartAuction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auction_manager = AuctionManager(bot)

    @app_commands.command(name="startauction", description="Mulai lelang baru")
    @app_commands.describe(
        item="Nama item",
        starting_bid="Harga awal",
        timer="Durasi dalam detik",
        min_increment="Minimal bid"
    )
    async def start_auction(self, interaction: discord.Interaction, 
                            item: str, 
                            starting_bid: int,
                            timer: int = None,
                            min_increment: int = None):
        # Cek peran admin
        if not any(role.id == ADMIN_ROLE_ID for role in interaction.user.roles):
            await interaction.response.send_message("Hanya admin yang bisa menggunakan command", ephemeral=True)
            return
        
        # Set default values
        min_increment = min_increment or 1000
        if timer is None:
            timer = AuctionModel.get_default_timer(interaction.guild_id) or DEFAULT_TIMER
        
        await interaction.response.send_message(
            f"⚡ Memulai lelang **{item}**...", 
            ephemeral=True
        )
        
        await self.auction_manager.start_auction(
            interaction,
            item,
            starting_bid,
            min_increment,
            timer
        )

async def setup(bot):
    await bot.add_cog(StartAuction(bot))