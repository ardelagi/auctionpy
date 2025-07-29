import asyncio
import discord
from bson import ObjectId
from models.auction import AuctionModel
from utils.formatter import format_rupiah
from utils.bid_parser import parse_bid

class AuctionManager:
    def __init__(self, bot):
        self.bot = bot
        self.active_timers = {}

    async def start_auction(self, interaction, item, starting_bid, min_increment, timer):
        channel = interaction.channel
        guild_id = interaction.guild_id
        
        embed = discord.Embed(
            title=f"🚀 Lelang Dimulai: {item}",
            color=discord.Color.gold()
        )
        embed.add_field(name="Harga Awal", value=format_rupiah(starting_bid), inline=True)
        embed.add_field(name="Min. Kenaikan", value=format_rupiah(min_increment), inline=True)
        embed.add_field(name="Waktu Tersisa", value=f"{timer} detik", inline=False)
        embed.set_footer(text="Kirim bid dengan mengetik angka (contoh: 50000, 100rb, 1.5jt)")
        
        message = await channel.send(embed=embed)
        
        auction_data = {
            "item": item,
            "starting_bid": starting_bid,
            "current_bid": starting_bid,
            "min_increment": min_increment,
            "timer": timer,
            "channel_id": channel.id,
            "message_id": message.id,
            "guild_id": guild_id,
            "isActive": True,
            "bids": [],
            "start_time": asyncio.get_event_loop().time(),
            "highest_bidder": None
        }
        
        auction_id = AuctionModel.create_auction(auction_data)
        self.start_timer(auction_id, timer)
        return auction_id

    def start_timer(self, auction_id, duration):
        async def countdown():
            await asyncio.sleep(duration)
            await self.end_auction(auction_id)
        
        task = asyncio.create_task(countdown())
        self.active_timers[auction_id] = task

    async def end_auction(self, auction_id):
        auction = AuctionModel.get_auction(auction_id)
        if not auction or not auction.get('isActive', True):
            return
        
        AuctionModel.stop_auction(auction_id)
        channel = self.bot.get_channel(auction['channel_id'])
        
        try:
            message = await channel.fetch_message(auction['message_id'])
        except discord.NotFound:
            return
        
        winner = auction.get('highest_bidder')
        winner_text = f"<@{winner}>" if winner else "Tidak ada pemenang"
        
        embed = discord.Embed(
            title=f"🏁 Lelang Selesai: {auction['item']}",
            color=discord.Color.green() if winner else discord.Color.red()
        )
        embed.add_field(name="Pemenang", value=winner_text, inline=True)
        embed.add_field(name="Harga Akhir", value=format_rupiah(auction['current_bid']), inline=True)
        
        await message.edit(embed=embed)
        
        if winner:
            await channel.send(f"🎉 Selamat <@{winner}>! Anda memenangkan lelang {auction['item']} dengan harga {format_rupiah(auction['current_bid'])}")

    async def process_bid(self, message):
        channel_id = message.channel.id
        auction = AuctionModel.get_active_auction(channel_id)
        
        if not auction:
            return
        
        bid_amount = parse_bid(message.content)
        if not bid_amount:
            return
        
        min_bid = auction['current_bid'] + auction['min_increment']
        
        if bid_amount < min_bid:
            reply = await message.reply(
                f"🚫 Bid harus lebih tinggi dari {format_rupiah(min_bid)}!",
                delete_after=5
            )
            await asyncio.sleep(5)
            await message.delete()
            return
        
        # Update auction
        AuctionModel.update_auction(auction['_id'], {
            "current_bid": bid_amount,
            "highest_bidder": message.author.id,
            "$push": {"bids": {
                "user_id": message.author.id,
                "amount": bid_amount,
                "timestamp": message.created_at.timestamp()
            }}
        })
        
        # Update embed
        try:
            auction_msg = await message.channel.fetch_message(auction['message_id'])
            embed = auction_msg.embeds[0]
            
            # Update fields
            embed.clear_fields()
            embed.add_field(name="Harga Terkini", value=format_rupiah(bid_amount), inline=True)
            embed.add_field(name="Min. Kenaikan", value=format_rupiah(auction['min_increment']), inline=True)
            embed.add_field(name="Bid Tertinggi", value=f"<@{message.author.id}>", inline=True)
            embed.add_field(name="Waktu Tersisa", value=f"{auction['timer']} detik", inline=False)
            
            await auction_msg.edit(embed=embed)
        except:
            pass
        
        # Delete bid message after delay
        await asyncio.sleep(5)
        try:
            await message.delete()
        except:
            pass