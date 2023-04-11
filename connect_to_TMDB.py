import requests
from passwords_and_keys import api_key_to_TMDB as apk

search_movie = 'https://api.themoviedb.org/3/search/movie'

movie = "avatar"
page_num = 1
total_movies = []

while True:
    #{search_movie}?api_key={apk}=en-US&query={movie}&page={page_num}&include_adult=false
    params = {
        "api_key": apk,
        "query": movie,
        "page": page_num
    }

    response = requests.get(search_movie, params=params)
    data = response.json()
    movies_list = data.get("results")
    if not movies_list:
        break

    total_movies.extend(movies_list)
    page_num += 1

print(f'Movies found: {len(total_movies)}')
for movie in total_movies:
    if "Avatar" in movie.get("title"):
        print(movie.get("title"))

