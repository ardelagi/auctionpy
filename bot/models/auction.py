from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
import time

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
auctions = db['auctions']
guild_settings = db['guild_settings']

class AuctionModel:
    @staticmethod
    def create_auction(data):
        return auctions.insert_one(data).inserted_id

    @staticmethod
    def update_auction(auction_id, update_data):
        return auctions.update_one({'_id': auction_id}, {'$set': update_data})

    @staticmethod
    def get_active_auction(channel_id):
        return auctions.find_one({'channel_id': channel_id, 'isActive': True})

    @staticmethod
    def stop_auction(auction_id):
        return auctions.update_one({'_id': auction_id}, {'$set': {'isActive': False}})
    
    @staticmethod
    def set_default_timer(guild_id, timer):
        guild_settings.update_one(
            {'guild_id': guild_id},
            {'$set': {'default_timer': timer}},
            upsert=True
        )
    
    @staticmethod
    def get_default_timer(guild_id):
        setting = guild_settings.find_one({'guild_id': guild_id})
        return setting.get('default_timer') if setting else None