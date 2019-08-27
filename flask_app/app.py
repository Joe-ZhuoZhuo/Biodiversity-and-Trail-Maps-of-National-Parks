import os

import pandas as pd
import numpy as np

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Ming: I'm putting this up here because the function takes a few seconds to run and it's better to have it run once when the server starts than every single time the user visits the API. (As the API won't need to be updated in real time) I'm basically cacheing the data. 

from Roger import rogers_func
rogers_dic = rogers_func()

# RL - The function below replaces Roger
from python_to_parent_child_JSON import return_json
species_data = return_json()


from serge import serges_func
jsons = serges_func()
parks_json = jsons["parks"]
species_json = jsons["species"]
cat_json = jsons["cat"]

@app.route("/")
def index():
    return render_template("index.html")

# Route for collapsible speciess tree
@app.route("/tree")
def build_tree():
    return render_template("tree.html")

# RL - This route is no longer needed
# @app.route("/roger")
# def roger():
#     return jsonify(rogers_dic)

@app.route("/parks")
def parks():
    return parks_json

@app.route("/species")
def species():
    # RL - This is from python_to_parent_child_JSON
    return jsonify(species_data)
#     return species_json

@app.route("/cat")
def cat():
     return cat_json


if __name__ == "__main__":
     app.run()

