#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, jsonify
from pprint import pprint 
import requests

app = Flask(__name__)

@app.route("/")
def home():
    # Get the weekly trending items (Include all movies, TV shows and people in the results as a global trending list). 
    trending = requests.get("https://api.themoviedb.org/3/trending/all/week?api_key=2e561a185b4300be1e527dbbcf9eadfd&language=fr-FR").json()
    trendingResult = trending["results"]  
    # Get a list of the current popular movies on TMDB. This list updates daily. 
    popularMovies = requests.get("https://api.themoviedb.org/3/movie/popular?api_key=2e561a185b4300be1e527dbbcf9eadfd&language=fr-FR").json()
    moviesResult = popularMovies["results"] 
    sortResult = mostPopularMovie(moviesResult)  

    return render_template('home.html', trending = trendingResult, mostPopularMovie=sortResult)

def mostPopularMovie(list):
    if (len(list) == 0): 
        return 0
    elif (len(list) == 1):
        return list[0]
    else: 
        # We search for the most popular film in the list
        m = list[0] 
        for p in list[1:]: 
            if(p["popularity"]>m["popularity"]):
                m=p
        print("The current popular movie on TMDB." + str(m))
        return m

if __name__ == '__main__':
    app.run(debug=True)
