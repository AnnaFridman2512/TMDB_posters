import base64
import pymongo
import requests
import io
from passwords_and_keys import mongo_db_password, username


password = mongo_db_password

# build the connection URI
uri = f'mongodb://localhost:27017/TMDB_posters'

# connect to the database using the URI
client = pymongo.MongoClient(uri)

# access a collection
db = client["TMDB_posters"]
collection = db["posters"]


def create_mongo_user():
    # Check if user exists
    users_dict = db.command("usersInfo")
    users_list = users_dict['users']

    if len(users_list) > 0:
        for user_dict in users_list:
            user_list_tup = user_dict.items()
            for user_data in user_list_tup:
                if user_data[0] == username:
                    print(f'User {username} already exists')
    else:
        # Create user with read/write permissions to 'TMDB_posters' database
        db.command("createUser", username, pwd=password, roles=[{"role": "readWrite", "db": "TMDB_posters"}])
        print(f'User {username} created successfully')

        # Update the URI with the new credentials
    updated_uri = f'mongodb://{username}:{password}@localhost:27017/TMDB_posters'
    return updated_uri


#create_mongo_user()
def delete_mongo_user(username):
    db.command("dropUser", username)
    print(f"User {username} has been deleted.")

#delete_mongo_user('user')

def get_all_posters():
    create_mongo_user()
    posters = list(collection.find())
    posters_dict = {}
    for poster in posters:
        poster_dict = {
            "movie_title": poster["movie_title"],
            "TMDB_id": poster["TMDB_id"],
            "poster": base64.b64encode(poster["poster"]).decode('utf-8')
        }
        posters_dict.update({poster["movie_title"]: poster_dict})

    #print(posters_dict)
    return posters_dict


#get_all_posters()
def find_poster_in_mongo(movie_title):
    create_mongo_user()
    movie_title = movie_title.lower()
    query = {"movie_title": movie_title}
    results = collection.find(query)
    results = list(results)
    if len(results) > 0:
        first_result = list(results)[0]
        return first_result


# find_poster_in_mongo("bla")

# define a function to save the image to MongoDB
def save_poster_to_mongo(movie):
    create_mongo_user()
    # download the image from poster_path
    response = requests.get(f"https://image.tmdb.org/t/p/original/{movie['poster_path']}")
    image_binary = io.BytesIO(response.content).getvalue()
    movie_title = movie["title"]
    # Each poster in mongo will look like this:
    document = {
        "movie_title": movie_title.lower(),
        "TMDB_id": movie["id"],
        "poster": image_binary
    }

    collection.insert_one(document)


"""movie = {'adult': False, 'backdrop_path': '/vL5LR6WdxWPjLPFRLe133jXWsh5.jpg', 'genre_ids': [28, 12, 14, 878],
         'id': 19996, 'original_language': 'en', 'original_title': 'ANNA',
         'overview': 'In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.',
         'popularity': 386.424, 'poster_path': '/jRXYjXNq0Cs2TcJjLkki24MLp7u.jpg', 'release_date': '2009-12-15',
         'title': 'AnnaAnna', 'video': False, 'vote_average': 7.569, 'vote_count': 28849}

save_poster_to_mongo(movie)"""


def delete_poster_from_mongo(title):
    create_mongo_user()
    collection.delete_one({"movie_title": title})
    return f'Movie {title} was deleted from mongoDB'

#delete_poster_from_mongo("scream")