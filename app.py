import base64

from connect_to_TMDB import find_movie
from flask import Flask, request, render_template, make_response

from connect_to_mongoDB import find_poster_in_mongo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/find_movie', methods=['POST'])
def find_movie():
    title = request.form['movie_title']
    movies = find_poster_in_mongo(title)
    if len(movies) > 0:
        movie = movies[0]
        response = make_response('<h1>{}</h1><img src="data:image/jpeg;base64,{}">'.format(movie['movie_title'],base64.b64encode(movie['poster']).decode()))
        response.headers['Content-Type'] = 'text/html'
        return response
    else:
        return 'Movie not found'


if __name__ == '__main__':
    app.run()
