from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]
auctions_collection = db['auctions']

class AuctionModel:
    @staticmethod
    def get_all_auctions():
        return list(auctions_collection.find({}))
    
    @staticmethod
    def get_active_auctions():
        return list(auctions_collection.find({'isActive': True}))
    
    @staticmethod
    def get_auction(auction_id):
        return auctions_collection.find_one({'_id': auction_id})
    
    @staticmethod
    def stop_auction(auction_id):
        return auctions_collection.update_one(
            {'_id': auction_id},
            {'$set': {'isActive': False}}
        )