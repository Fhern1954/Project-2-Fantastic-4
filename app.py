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
    final_list = ["All"] + unique_country_list
    sorted_country_dict["country"] = final_list
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
    final_list = ["All"] + unique_genre_list
    sorted_genre_dict["genre"] = final_list
    return jsonify(sorted_genre_dict)

@app.route("/year")
def year():

    data = mongo.db.movies.find().distinct('year')
    year_list = list(data)
    sorted_year_dict = {}
    sorted_year_dict["year"] = year_list
    return jsonify(sorted_year_dict)             
   
@app.route("/top_movies_table")
def countries_table_top10():
    query_string = request.args
    print(query_string)
    mongo_query = {"votes": {"$gte":"200"}}
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
    table_response = []
    for document in sorted_data:
        table_response.append({
            "title": document["title"],
            "country": document["country"],
            "genre": document["genre"],
            "year":document["year"],
            "rating":document["avg_vote"],
            "numberofvotes":document["votes"]

        })
        # print(document["title"], document["country"], document["genre"])

    return jsonify(table_response)

@app.route("/top_movies_graph")
def countries_graph_top10():
    query_string = request.args
    print(query_string)
    mongo_query = {"votes": {"$gte":"200"}}
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
    graph_response = []
    for document in sorted_data:
        graph_response.append({
            "title": document["title"],
            "budget":document["budget"],
            "worldwide_gross_income": document["worlwide_gross_income"]

        })
        # print(document["title"], document["country"], document["genre"])

    return jsonify(graph_response)    
    

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

@app.route("/movies_map")
def countries_map():
    country_count = {}
    query_string = request.args
    print(query_string)
    mongo_query = {"votes": {"$gte":"200"}}
    for k, v in query_string.items():
        if k == "genre":
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
    sorted_data = list(data)

    countries = mongo.db.movies.find().distinct('country')
    country_list = list(countries)
    unique_country_list = []
    sorted_country_dict = {}
    # Iterate through the outer list
    for countries in country_list:
        c = countries.split(', ')
        for c_list in c:
            if c_list != "":
                if c_list not in unique_country_list:
                    unique_country_list.append(c_list)
                    country_count[c_list] = 0;
    unique_country_list.sort()
    
    for result in sorted_data:
        for country in unique_country_list:
            if country in result["country"]:
                country_count[country] += 1;


    # map_response = []
    # for document in sorted_data:
    #     map_response.append({
    #         "country": document["country"]
    #     })
        # print(document["title"], document["country"], document["genre"])
    return jsonify(country_count)                         
      


if __name__ == "__main__":
    app.run(debug=True)