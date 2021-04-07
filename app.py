from flask import Flask, render_template, redirect, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from bson.json_util import dumps
from bson.json_util import loads

# Create an instance of Flask
app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_ORIGINS'] = '*'
app.config['DEBUG'] = True

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

@app.route("/countries")
def countries():

    data = mongo.db.movies.find().distinct('country')
    country_list = list(data)
    unique_country_list = []
    sorted_country_dict = {}
    # Iterate through the outer list
    for countries in country_list:
        c = countries.split(', ')
        for c_list in c:
            if c_list != "":
                if c_list not in unique_country_list:
                    unique_country_list.append(c_list)
    unique_country_list.sort()
    sorted_country_dict["country"] = unique_country_list
    return jsonify(sorted_country_dict)  


@app.route("/genres")
def genres():

    data = mongo.db.movies.find().distinct('genre')
    genre_list = list(data)
    unique_genre_list = []
    sorted_genre_dict = {}
    # Iterate through the outer list
    for genres in genre_list:
        g = genres.split(', ')
        for genre_list in g:
            if genre_list != "":
                if genre_list not in unique_genre_list:
                    unique_genre_list.append(genre_list)
    unique_genre_list.sort()
    sorted_genre_dict["genre"] = unique_genre_list
    return jsonify(sorted_genre_dict)

@app.route("/year")
def year():

    data = mongo.db.movies.find().distinct('year')
    year_list = list(data)
    sorted_year_dict = {}
    sorted_year_dict["year"] = year_list
    return jsonify(sorted_year_dict)             
   
@app.route("/top_movies")
def countries_top10():
    query_string = request.args
    print(query_string)
    mongo_query = {"votes": {"$gte":"300"}}
    for k, v in query_string.items():
        if k == "country":
            mongo_query["country"] = v
        elif k == "genre":
            mongo_query["genre"] = v
        elif k == "startyear":
            if "year" in mongo_query:
                mongo_query["year"]["$gte"] = v
            else:
                mongo_query["year"] = {"$gte":v}
        elif k == "endyear":
            if "year" in mongo_query:
                mongo_query["year"]["$lte"] = v
            else:
                mongo_query["year"] = {"$lte":v}
                
            
    data = mongo.db.movies.find(mongo_query)
    sorted_data = list(data.sort("avg_vote",-1)[0:10])
    response = []
    for document in sorted_data:
        response.append({
            "title": document["title"],
            "country": document["country"],
            "genre": document["genre"],
            "year":document["year"]
        })
        print(document["title"], document["country"], document["genre"])


    # topmovies_bycountry = []
    # topmovies = {}
    # # display_data = sorted_data["imdb_title_id","original_title","year","avg_vote","votes"]
    # # box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]
    # json_data = dumps(sorted_data)
    # # for data in json_data:
    # #     topmovies_bycountry.append(json_data[data])
    # # for topmov in sorted_data:
    # #     tm = topmov.split('_id')
    # #     for tm_list in tm:
    # #         topmovies_bycountry.append(tm_list)
    # # topmovies["movies"] = topmovies_bycountry 
    # topmovies["movies"] = json_data 
    return jsonify(response)
    

@app.route("/top_movies_by_genre/<genre>")
def genres_top10(genre):

    data = mongo.db.movies.find().distinct('genre')
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]

    return jsonify(display_data,box_office_data)      

@app.route("/top_movies_country_genre/<country>/<genre>")
def top_movies_country_genre(country, genre):

    data = mongo.db.movies.find({"country": country,"genre":genre})
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]

    return jsonify(display_data,box_office_data) 
    
@app.route("/top_movies_year/<startyear>/<endyear>")
def top_movies_year(startyear, endyear):

    startyear = startyear.astype('int64')
    endyear = endyear.astype('int64')
    data = mongo.db.movies.find({"year": {"$gte": startyear, "$lte": endyear}})
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]

    return jsonify(display_data,box_office_data)

@app.route("/top_movies_country_year/<country>/<startyear>/<endyear>")
def top_movies_country_year(country,startyear,endyear):

    startyear = startyear.astype('int64')
    endyear = endyear.astype('int64')
    data = mongo.db.movies.find({"year": {"$gte": startyear, "$lte": endyear},"country":country})
    sorted_data = list(data.sort("avg_vote", -1)[0:10])
    display_data = sorted_data["imdb_title_id","original_title","year","country","genre","avg_vote","votes"]
    box_office_data = sorted_data["imdb_title_id","original_title","budget","worldwide_gross_income"]

    return jsonify(display_data,box_office_data)

@app.route("/top_movies/<genre>/<startyear>/<endyear>")
def top_movies_genre_year(genre,year):

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