import discord
from discord import app_commands
from discord.ext import commands
from models.auction import AuctionModel
from utils.auction_manager import AuctionManager
from config import ADMIN_ROLE_ID

class StopAuction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auction_manager = AuctionManager(bot)

    @app_commands.command(name="stopauction", description="Hentikan lelang aktif")
    async def stop_auction(self, interaction: discord.Interaction):
        if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("❌ Hanya admin yang bisa menggunakan perintah ini!", ephemeral=True)
            return
        
        auction = AuctionModel.get_active_auction(interaction.channel_id)
        if not auction:
            await interaction.response.send_message("ℹ️ Tidak ada lelang aktif di channel ini", ephemeral=True)
            return
        
        await self.auction_manager.end_auction(auction['_id'])
        await interaction.response.send_message("🛑 Lelang dihentikan!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(StopAuction(bot))