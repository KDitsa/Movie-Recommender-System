from .myapi import api
from tmdbv3api import TMDb, Movie
import pandas as pd

tmdb = TMDb()
tmdb.api_key = api

movie_search = Movie()

def get_poster_url(movie_title):
    results = movie_search.search(movie_title)
    if results:
        poster_path = results[0].poster_path
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None