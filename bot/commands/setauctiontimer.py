import discord
from discord import app_commands
from discord.ext import commands
from models.auction import AuctionModel
from config import ADMIN_ROLE_ID

class SetAuctionTimer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setauctiontimer", description="Set default timer untuk lelang")
    @app_commands.describe(timer="Durasi default dalam detik")
    async def set_auction_timer(self, interaction: discord.Interaction, timer: int):
        if not any(role.id == ADMIN_ROLE_ID for role in interaction.user.roles):
            await interaction.response.send_message("Hanya admin yang bisa menggunakan command", ephemeral=True)
            return
        
        AuctionModel.set_default_timer(interaction.guild_id, timer)
        await interaction.response.send_message(
            f"timer diatur menjadi **{timer} detik**",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(SetAuctionTimer(bot))