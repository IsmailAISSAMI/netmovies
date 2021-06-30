#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, jsonify
from pprint import pprint 
import requests

app = Flask(__name__)

@app.route("/")
def home():
    res = requests.get("https://api.themoviedb.org/3/trending/all/week?api_key=2e561a185b4300be1e527dbbcf9eadfd&language=fr-FR").json()
    data = res["results"]    
    print("success")
    return render_template('home.html', trending = data)

if __name__ == '__main__':
    app.run(debug=True)
