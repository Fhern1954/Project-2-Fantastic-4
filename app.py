from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb+srv://fan4_mongo:sGWQhhfqSBAcmFFn@cluster0.eqase.mongodb.net/movie_db")


# destination_data = mongo.db.movies.find({'country': "USA", "genre": "Romance"})
# sorted_data = list(destination_data.sort("avg_vote", -1)[0:10])
#print(sorted_data)
# print("length:", len(sorted_data))

# for document in sorted_data:
    # print(document["title"], document["country"], document["genre"])

@app.route("/")
def main():

    data = mongo.db.movies
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]
    return jsonify(display_data,box_office_data) 
   
@app.route("/top_movies/<countries>")
def countries():

    data = mongo.db.movies.find().distinct('country')
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]

    return jsonify(display_data,box_office_data) 
    

@app.route("/top_movies/<genre>")
def genres():

    data = mongo.db.movies.find().distinct('genre')
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]

    return jsonify(display_data,box_office_data)      

@app.route("/top_movies/<country>/<genre>")
def top_movies(country, genre):

    data = mongo.db.movies.find({"country": country,"genre":genre})
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]

    return jsonify(display_data,box_office_data) 
    
@app.route("/top_movies/<startyear>/<endyear>")
def top_movies(year):

    startyear = startyear.astype('int64')
    endyear = endyear.astype('int64')
    data = mongo.db.movies.find({"year": {"$gte": startyear, "$lte": endyear}})
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]

    return jsonify(display_data,box_office_data)

@app.route("/top_movies/<country>/<startyear>/<endyear>")
def top_movies(country,year):

    startyear = startyear.astype('int64')
    endyear = endyear.astype('int64')
    data = mongo.db.movies.find({"year": {"$gte": startyear, "$lte": endyear},"country":country})
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]

    return jsonify(display_data,box_office_data)

@app.route("/top_movies/<genre>/<startyear>/<endyear>")
def top_movies(genre,year):

    startyear = startyear.astype('int64')
    endyear = endyear.astype('int64')
    data = mongo.db.movies.find({"year": {"$gte": startyear, "$lte": endyear},"genre":genre})
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]

    return jsonify(display_data,box_office_data) 

@app.route("/top_movies/<country>/<genre>/<startyear>/<endyear>")
def top_movies(country,genre,year):

    startyear = startyear.astype('int64')
    endyear = endyear.astype('int64')
    data = mongo.db.movies.find({"year": {"$gte": startyear, "$lte": endyear},"country":country,"genre":genre})
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]

    return jsonify(display_data,box_office_data)                      
      


if __name__ == "__main__":
    app.run(debug=True)