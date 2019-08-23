#Ming: I'm putting this stuff aside for later in case we need it. 

#If this was a startup that we were going to continue developing, I'd suggest separating the ETL process from the web process so someone could update the database without touching the front end and the front end would always get the latest data. You'll just have to restart the server for that to happen now. This is mostly due to time constraints.

# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine


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