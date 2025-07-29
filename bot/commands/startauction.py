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
        starting_bid="Harga awal (angka)",
        timer="Durasi dalam detik (opsional)",
        min_increment="Kenaikan minimal (opsional)"
    )
    async def start_auction(self, interaction: discord.Interaction, 
                            item: str, 
                            starting_bid: int,
                            timer: int = None,
                            min_increment: int = None):
        # Check admin role
        if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("❌ Hanya admin yang bisa menggunakan perintah ini!", ephemeral=True)
            return
        
        # Set default values
        min_increment = min_increment or 1000
        if timer is None:
            timer = AuctionModel.get_default_timer(interaction.guild_id) or DEFAULT_TIMER
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        try:
            auction_id = await self.auction_manager.start_auction(
                interaction,
                item,
                starting_bid,
                min_increment,
                timer
            )
            await interaction.followup.send(f"⚡ Lelang untuk **{item}** telah dimulai!", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Gagal memulai lelang: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(StartAuction(bot))