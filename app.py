import base64
from flask import Flask, request, render_template, make_response, jsonify
from flask_httpauth import HTTPBasicAuth
from connect_to_TMDB import find_poster
from connect_to_mongoDB import save_poster_to_mongo, delete_poster_from_mongo, get_all_posters
from passwords_and_keys import username, mongo_db_password as password

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(user, psw):
    # Check the username and password against your MongoDB user
    return user == username and psw == password
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/find_movie', methods=['POST'])
def find_movie():
    title = request.form['movie_title']
    movie = find_poster(title)
    if type(movie) == dict: #If we found the movie in mongo we get a dict as a return value
        response = make_response('<h1>Movie {} found in Mongo</h1><img src="data:image/jpeg;base64,{}">'.format(movie['movie_title'],base64.b64encode(movie['poster']).decode()))
    elif "https" in movie[1]:#if we found the movie in TMDB we get a list [movie_title, poster_url]
        movie_title, poster_url, movie_dict = movie
        save_poster_to_mongo(movie_dict)
        response = make_response('<h1>Movie {} found in TMDB, and added to mongo</h1><img src="{}">'.format(movie_title, poster_url))
    else:#if movie isn't found - just show the error message that we resive from find_poster function (if not movies_list:)
        response = make_response('<h1>{}</h1>'.format(movie))
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route('/posters')
@auth.login_required
def get_all_posters_route():
    posters = get_all_posters()
    return jsonify(posters)



@app.route('/delete_poster', methods=['POST'])
def delete_poster():
    title = request.form['movie_title']
    deleted = delete_poster_from_mongo(title)
    if deleted:
        return '<h1>Poster deleted from MongoDB</h1>'
    else:
        return '<h1>Error: Poster not found in MongoDB</h1>'

if __name__ == '__main__':
    app.run(debug=True)

