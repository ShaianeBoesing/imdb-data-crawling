import json

with open("./movies_data/imdb.json", "rb") as file:
    imdb_data = json.load(file)

with open("./movies_data/tomato.json", "rb") as file:
    tomato_data = json.load(file)

unified_data = []

movie_template = {
    "Title": "",
    "Release Dates": [],
    "Runtime": "",
    "age_rating": "",
    "Genres": [],
    "Actors": [],
    "IMDB_score": "",
    "Tomatometer": "",
    "Popcornmeter": "",
}

for imdb_movie in imdb_data:
    for tomato_movie in tomato_data:
        if imdb_movie["Title"] == tomato_movie["Title"] and imdb_data["Release Dates"] == tomato_movie["Release Dates"]:
            