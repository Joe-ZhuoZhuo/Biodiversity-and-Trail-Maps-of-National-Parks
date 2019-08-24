import os

import pandas as pd
import numpy as np

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Ming: I'm putting this up here because the function takes a few seconds to run and it's better to have it run once when the server starts than every single time the user visits the API. (As the API won't need to be updated in real time) I'm basically cacheing the data. 
#+======UNCOMMENT THIS LATER FOR ROGER
# from Roger import rogers_func
# rogers_dic = rogers_func()

# Ming: Same here, get the stuff done before server hosts the website. Serge function has both parks and species inside but currently only returns parks. Can change if needed later. See further comments in serge.py
from serge import serges_func
parks_json = serges_func()

@app.route("/")
def index():
    return render_template("index.html")
#+======UNCOMMENT THIS LATER FOR ROGER
# @app.route("/roger")
# def roger():
#     return jsonify(rogers_dic)

@app.route("/parks")
def parks():
    return parks_json


if __name__ == "__main__":
     app.run()