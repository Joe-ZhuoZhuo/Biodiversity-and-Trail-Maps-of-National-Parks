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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/parks_and_species.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
parks_metadata = Base.classes.parks
species_metadata = Base.classes.species
# Samples = Base.classes.samples


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")



@app.route("/metadata/state/<state>")
def parks_by_state(state):

    stmt = db.session.query(park_metadata).statement
    sp_stmt = db.session.query(species_metadata).statement

    df = pd.read_sql_query(stmt, db.session.bind)
    df_sp = pd.read_sql_query(sp_stmt, db.session.bind)

    sample_data = df.loc[df['State'] == state, :]
    sample_data_sp = df_sp.loc[df_sp['State'] == state, :]


    parks = sample_data.values[0][2:]
    species = sample_data_sp.values[0][2:]

    data = {
        'parks': parks.tolist(),
        'species': species.tolist()
    }

    return jsonify(data)


@app.route("/states")
def states():
    sel = [park_metadata.State]

    states = [state[0] for state in db.session.query(*sel).all()]

    return jsonify(states)



if __name__ == "__main__":
    app.run()