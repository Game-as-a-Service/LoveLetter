import pymongo
from pymongo.server_api import ServerApi

from love_letter.config import settings


db = pymongo.MongoClient(settings.MONGODB_URL, server_api=ServerApi('1')).get_default_database()

# col = db["customer"]
# mydict = {"name": "John", "address": "Highway 37"}

# x = db.customer.insert_one(mydict)
# print(x)

# for i in db.customer.find({}):
#     print(i)

# db.customer.delete_many({"id": 1})
# db.customer.delete_many({"name": 'John'})
