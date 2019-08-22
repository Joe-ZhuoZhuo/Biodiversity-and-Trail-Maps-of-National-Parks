import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/parks_and_species.sqlite"
# db = SQLAlchemy(app)

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# # Save references to each table
# parks_metadata = Base.classes.parks
# species_metadata = Base.classes.species
# # Samples = Base.classes.samples


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")



@app.route("/roger")
def roger():
    import pandas as pd
    import json
    df = pd.read_csv('resources/species.csv', low_memory=False)
    # choose columns to keep, in the desired nested json hierarchical order
    df = df[['Park Name', 'Category', 'Order', 'Family', 'Common Names']]
    # order in the groupby here matters, it determines the json nesting
    # the groupby call makes a pandas series by grouping “category”, “sub_category” and”sub_category_type”,
    #while summing the numerical column 'count'
    df1 = df.groupby(['Park Name', 'Category', 'Order', 'Family'])['Common Names'].unique()
    df1 = df1.reset_index()
    # print(df1)
    d = dict()
    d = {'children': []}
    for line in df1.values:
        category = line[0]
        sub_category = line[1]
        sub_category_type = line[2]
        count = line[3]
        # make a list of keys
        category_list = []
        for item in d['children']:
            category_list.append(item['name'])
        # if 'category' is NOT category_list, append it
        if not category in category_list:
            d['children'].append({'name':category, 'children':[{'name':sub_category, 'children':[{'name': sub_category_type}]}]})
        # if 'category' IS in category_list, add a new child to it
        else:
            sub_list = []
            for item in d['children'][category_list.index(category)]['children']:
                sub_list.append(item['name'])
            # print sub_list
            if not sub_category in sub_list:
                d['children'][category_list.index(category)]['children'].append({'name':sub_category, 'children':[{'name': sub_category_type}]})
            else:
                d['children'][category_list.index(category)]['children'][sub_list.index(sub_category)]['children'].append({'name': sub_category_type})
     #print(json.dumps(d))
    return jsonify(d)




if __name__ == "__main__":
     app.run()