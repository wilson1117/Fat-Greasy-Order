import pymongo
from bson.objectid import ObjectId


class OrderDB:
    def __init__(self, server="localhost:27017", db="order"):
        self.db = pymongo.MongoClient(f"mongodb://{server}")[db]

    def get_food_info(self, name):
        return self.db["menu"].find_one({"name": name})

    def get_option(self, id):
        return self.db["options"].find_one({"_id": [ObjectId(id), id][type(id) == ObjectId]})

# mongo = pymongo.MongoClient("mongodb://localhost:27017")


if __name__ == "__main__":
    order = OrderDB()
    print([order.get_option(id)
           for id in order.get_food_info("肥宅快樂水")["options"]])
    # print(order.get_option("5edda630338a12e97ab1a901"))
