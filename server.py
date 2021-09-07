#!/usr/bin/env python
# -*- coding: utf-8 -*-

# packages
from flask import Flask, render_template, jsonify, redirect, url_for, request
from pprint import pprint 
import requests
import sqlite3
# Methods
from middlewares import *

app = Flask(__name__)

# database init
def __init__(self):
    con = sqlite3.connect('netmovie.db')
    c = con.cursor()
    req = "create table users(id INTEGER PRIMARY KEY AUTOINCREMENT, firstName TEXT NOT null, lastName TEXT NOT null, email text not null, password text not null);"
    c.execute(req)
    con.commit()


@app.route("/")
def home():
    # Get the weekly trending items (Include all movies, TV shows and people in the results as a global trending list). 
    trending = requests.get("https://api.themoviedb.org/3/trending/all/week?api_key=2e561a185b4300be1e527dbbcf9eadfd&language=fr-FR").json()
    trendingResult = trending["results"]  
    # Get a list of the current popular movies on TMDB. This list updates daily. 
    popularMovies = requests.get("https://api.themoviedb.org/3/movie/popular?api_key=2e561a185b4300be1e527dbbcf9eadfd&language=fr-FR").json()
    moviesResult = popularMovies["results"] 
    sortResult = mostPopularMovie(moviesResult)
    # Get the trailer of the most popular movie by its id, because we don't have the link in the previous request 
    trailer =  requests.get("https://api.themoviedb.org/3/movie/"+str(sortResult["id"])+"?api_key=2e561a185b4300be1e527dbbcf9eadfd&language=fr-FR").json()
    return render_template('home.html', mostPopularMovie=sortResult, mostPopularMovieTrailer= trailer["homepage"], trending = trendingResult)

@app.route("/movie/<id>")
def movie(id):
    if id is None:
        return render_template('404.html'), 404
    else:
        data =  requests.get("https://api.themoviedb.org/3/movie/"+id+"?api_key=2e561a185b4300be1e527dbbcf9eadfd&language=fr-FR").json()
        return render_template('movie.html', movie=data)


@app.route("/login", methods=['POST', 'GET'])
def login():
    con = sqlite3.connect('netmovie.db')
    c = con.cursor()
    
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']

        if(email!="" and password!=""):
            c.execute("SELECT * from users WHERE email=?  AND password=?;", (email, password))
            data = c.fetchone()
            if data:
                msg="Vous êtes bien connecté!"
                type= "success"
            else: 
                if not data:
                    msg="Votre email ou votre mot de passe n'est pas correct!"
                    type= "error"
        return render_template('login.html', msg=msg, type=type), 200

    else: 
        return render_template('login.html'), 200

@app.route("/register", methods=['POST', 'GET'])
def register():
    con = sqlite3.connect('netmovie.db')
    c = con.cursor()
    
    if request.method == 'POST':
        firstName = request.form['inputFirstName']
        lastName = request.form['inputLastName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        if(email!="" and password!=""):
            c.execute("SELECT * from users WHERE email=?  AND password=?;", (email, password))
            data = c.fetchone()
            if data:
                msg="Il existe déjà un compte avec cette Email!"
                type= "error"
            else: 
                if not data:
                    c.execute("INSERT INTO users (firstName, lastName, email, password) VALUES (?,?,?,?)", (firstName, lastName, email, password))
                    con.commit()
                    con.close()
                    msg="Votre compte a été bien enregistrer"
                    type= "success"
        return render_template('register.html', msg=msg, type=type), 200    
    else:
        return render_template('register.html'), 200    
    

# Render a personalized template for 404 status code.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
