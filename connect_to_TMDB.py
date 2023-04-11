import requests
from passwords_and_keys import api_key_to_TMDB as apk

def find_movie(movie_title):
    search_movie = 'https://api.themoviedb.org/3/search/movie'
    page_num = 1
    total_movies = []
    movie_titles = []

    while True:
        #{search_movie}?api_key={apk}=en-US&query={movie_title}&page={page_num}&include_adult=false
        params = {
            "api_key": apk,
            "query": movie_title,
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
        if movie_title in movie.get("title"):
            title = movie.get("title")
            movie_titles.append(title)
    #print(total_movies)
    #print(movie_titles)
    return total_movies, movie_titles


#find_movie("Avatar")