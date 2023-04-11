import pymongo
from passwords import mongo_db_password as mpw

username = "user"
password = mpw

# build the connection URI
uri = f'mongodb://{username}:{mpw}@localhost:27017/TMDB_posters'

# connect to the database using the URI
client = pymongo.MongoClient(uri)

# access a collection
db = client["TMDB_posters"]
collection = db["posters"]

