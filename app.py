from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb+srv://fan4_mongo:sGWQhhfqSBAcmFFn@cluster0.eqase.mongodb.net/movie_db")


destination_data = mongo.db.movies.find({'country': "USA", "genre": "Romance"})
sorted_data = list(destination_data.sort("avg_vote", -1)[0:10])
#print(sorted_data)
print("length:", len(sorted_data))

for document in sorted_data:
    print(document["title"], document["country"], document["genre"])

@app.route("/")
def main():

    render_template()

@app.route("/countries")
def countries():
    data = mongo.db.movies.find().distinct('country')

    return jsonify(data)  

@app.route("/genres")
def genres():
    data = mongo.db.movies.find().distinct('genre')

    return jsonify(data)       

@app.route("/top_movies/<country>/<genre>")
def top_movies(country, genre):
    data = mongo.db.movies.find({"country": country})

    return jsonify(data)

@app.route("/top_movies_country/<country>")
def top_movies_country(country):
    data = mongo.db.movies.find({"country": country})

    return jsonify(data)    

@app.route("/top_movies_genre/<genre>")
def top_movies_genre(genre):
    data = mongo.db.movies.find({"genre": genre})

    return jsonify(data)       


if __name__ == "__main__":
    app.run(debug=True)