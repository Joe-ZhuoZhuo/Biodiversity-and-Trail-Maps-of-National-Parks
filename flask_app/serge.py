def serges_func():
	import pandas as pd
	import sqlite3, matplotlib
	from sqlalchemy import create_engine
	import re
	df_pr = pd.read_csv('resources/parks.csv', encoding='utf-8')
	  
	df_sp = pd.read_csv('resources/species.csv', encoding='utf-8')

	df_pr.rename(columns={'Park Code':'park_code','Park Name':'park_name','State':'state','Acres':'acres','Latitude':'latitude','Longitude':'longitude'}, inplace=True)

	df_sp.drop(['Unnamed: 13'], axis=1, inplace=True)

	df_sp.rename(columns={'Species ID':'species_ID','Park Name':'park_name','Category':'category','Order':'order','Family':'family','Scientific Name':'scientific_name','Common Names':'common_names','Record Status':'record_status','Occurence':'occurence','Nativeness':'nativeness','Abundance':'abundance','Seasonability':'seasonability','Conservation Status':'conservation_status'}, inplace=True)

	df_sp.drop(['species_ID','scientific_name','record_status','Occurrence',
	       'nativeness', 'abundance', 'Seasonality', 'conservation_status'], axis=1, inplace=True)
	df_pr= df_pr.iloc[:,0:6]
	
	df_pr_sp = pd.merge(df_pr, df_sp)
	df_pr_sp.drop(['park_code','order','family'], axis=1, inplace=True)



	df_cat = df_pr_sp.groupby(['park_name', 'category'])[['category']].count()
	df_cat.to_csv("resources/cat.csv", index=True)
	cat_csv = pd.read_csv('resources/cat.csv')

	parks_json = df_pr.to_json(orient='records')
	cat_json = cat_csv.to_json(orient='records')

	species_json = df_sp.to_json(orient='records')
	return {"parks":parks_json, "cat":cat_json}


#====================================================
	# #SQL Stuff, not used currently

	# engine = create_engine('sqlite:///parks_and_species.db', echo=True)
	# df_pr.to_sql('parks', con=engine, if_exists='replace')
	# df_sp.to_sql('species', con=engine, if_exists='replace')
	# engine.execute("SELECT * FROM parks").fetchall()
	# engine.execute("SELECT * FROM species").fetchall()
	# engine.execute("SELECT * FROM species where park_name = 'Acadia National Park'").fetchall()
