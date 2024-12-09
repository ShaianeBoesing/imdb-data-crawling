"""
Módulo responsável por unificar os dados dos filmes do IMDB e do Rotten Tomatoes.
Alunos:
    Matheus Eduardo Lafeta Feliciano (21202339)
    Shaiane Boesing Rodrigues Borges (21202341)
"""

import json
from copy import deepcopy

from rapidfuzz import fuzz

with open("./movies_data/imdb.json", "rb") as file:
    imdb_data = json.load(file)

with open("./movies_data/tomato.json", "rb") as file:
    tomato_data = json.load(file)

unified_data = []


def merge_similarities_in_set(set_to_sanitize, ratio=80):
    """
    Recebe um set e o sanitiza removendo possíveis duplicatas a partir de uma ratio de similaridade.
    """
    set_copy = deepcopy(set_to_sanitize)
    itens_removed = []
    for item1 in set_to_sanitize:
        for item2 in set_to_sanitize:
            if fuzz.ratio(item1, item2) >= ratio and item2 not in itens_removed:
                set_copy.add(max(item1, item2))
                itens_removed.append(item2)
    print(set_copy)
    return set_copy


def create_merged_movie(
    title="",
    theaters_release_date="",
    streaming_release_date="",
    runtime="",
    age_rating="",
    genres=None,
    actors=None,
    imdb_score="",
    tomatometer="",
    popcornmeter="",
):
    """
    Cria um dicionário com os dados do filme no formato esperado.
    """
    if genres is None:
        genres = set()
    if actors is None:
        actors = set()

    movie_template = {
        "Title": title,
        "Theaters release Date": theaters_release_date,
        "Streaming release Date": streaming_release_date,
        "Runtime": runtime,
        "age_rating": age_rating,
        "Genres": genres,
        "Actors": actors,
        "IMDB_score": imdb_score,
        "Tomatometer": tomatometer,
        "Popcornmeter": popcornmeter,
    }
    return movie_template


for imdb_index, imdb_movie in enumerate(deepcopy(imdb_data)):
    for tomato_index, tomato_movie in enumerate(deepcopy(tomato_data)):
        tomato_theaters_release_date = ""
        tomato_streaming_release_date = ""

        for release_date in tomato_movie["Release Dates"]:
            if "Theaters:" in release_date:
                tomato_theaters_release_date = release_date.split(",")[1].strip()
            elif "Streaming:" in release_date:
                tomato_streaming_release_date = release_date.split(",")[1].strip()

        if (
            fuzz.ratio(imdb_movie["Title"], tomato_movie["Title"]) >= 90
            and imdb_movie["Release Dates"] == tomato_theaters_release_date
        ):
            movie_to_add = create_merged_movie(
                title=imdb_movie["Title"],
                theaters_release_date=tomato_theaters_release_date,
                streaming_release_date=tomato_streaming_release_date,
                runtime=imdb_movie["Runtime"],
                age_rating=imdb_movie["Rating"],
                genres=merge_similarities_in_set(
                    set(imdb_movie["Genres"] + tomato_movie["Genres"]), ratio=90
                ),
                actors=merge_similarities_in_set(
                    set(imdb_movie["Actors"] + tomato_movie["Actors"])
                ),
                imdb_score=imdb_movie["imdb_score"],
                tomatometer=tomato_movie["Tomatometer"],
                popcornmeter=tomato_movie["Popcornmeter"],
            )

            unified_data.append(movie_to_add)
            del imdb_data[imdb_index]
            del tomato_data[tomato_index]

for imdb_movie in imdb_data:
    movie_to_add = create_merged_movie(
        title=imdb_movie["Title"],
        theaters_release_date=imdb_movie["Release Dates"],
        runtime=imdb_movie["Runtime"],
        age_rating=imdb_movie["Rating"],
        genres=imdb_movie["Genres"],
        actors=imdb_movie["Actors"],
        imdb_score=imdb_movie["imdb_score"],
    )
    unified_data.append(movie_to_add)

for tomato_movie in tomato_data:
    tomato_theaters_release_date = ""
    tomato_streaming_release_date = ""
    for release_date in tomato_movie["Release Dates"]:
        if "Theaters:" in release_date:
            tomato_theaters_release_date = release_date.split(",")[1].strip()
        elif "Streaming:" in release_date:
            tomato_streaming_release_date = release_date.split(",")[1].strip()

    movie_to_add = create_merged_movie(
        title=tomato_movie["Title"],
        theaters_release_date=tomato_theaters_release_date,
        streaming_release_date=tomato_streaming_release_date,
        runtime=tomato_movie["Runtime"],
        genres=tomato_movie["Genres"],
        actors=tomato_movie["Actors"],
        tomatometer=tomato_movie["Tomatometer"],
        popcornmeter=tomato_movie["Popcornmeter"],
    )
    unified_data.append(movie_to_add)

for movie in unified_data:
    movie["Genres"] = list(movie["Genres"])
    movie["Actors"] = list(movie["Actors"])
with open("./movies_data/unified.json", "w", encoding="utf-8") as file:
    json.dump(unified_data, file, ensure_ascii=False, indent=4)
