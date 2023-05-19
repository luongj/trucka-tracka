#!/usr/bin/env python3
import pandas as pd
import sqlite3
import geopy.distance
import sys

###
# sqlite setup
#
file_sqlite3 = 'trucka-tracka.db'
sqlite_conn = sqlite3.connect(file_sqlite3)
sqlite_conn.row_factory = sqlite3.Row

###
# statics
#
file_csv_mobile_food = 'Mobile_Food_Facility_Permit.csv'
db_table_mobile_food = 'Mobile_Food_Facility_Permit' 

###
# functions
#
def upload_csv_to_sqlite(sqlcon = None, file_csv = None, db_table = None):
	mobile_food_data = pd.read_csv(file_csv, skiprows = 0, encoding='latin-1')
	mobile_food_data.columns = [c.replace(' ', '_') for c in mobile_food_data]

	mobile_food_data.to_sql(name = db_table, con=sqlcon, index=False, if_exists='replace')

def get_location_search_term(sqlcon = None, search = None):
	# https://stackoverflow.com/questions/45343175/python-3-sqlite-parameterized-sql-query
	# parameterizing with `LIKE` is messy; fix later
	return sqlcon.execute(
		f"""
		SELECT 	locationid, Applicant, Address, permit, Location, Latitude, Longitude
		FROM 	Mobile_Food_Facility_Permit
		WHERE 	1=1
 		AND 	Status IN ('APPROVED', 'ISSUED')
		AND 	lower(FoodItems) LIKE '%""" + search.lower() + "%'")

# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def get_distance_feet(location_1 = None, location_2 = None):
	return geopy.distance.geodesic(location_1, location_2).ft

###
# ====== MAIN ======
#

# check if data is loaded; if not, load database
query_result = sqlite_conn.execute("SELECT name FROM sqlite_master WHERE type = ? AND name = ?", ('table', db_table_mobile_food)).fetchall()
if len(query_result) == 0:
	upload_csv_to_sqlite(sqlcon = sqlite_conn, file_csv = file_csv_mobile_food, db_table = db_table_mobile_food)

###
# inputs; set some defaults
#
input_search = 'taco'
input_distance = 5000
input_search = input('What are you in the mood for? ')
input_distance = input('How far are you willing to go (in feet)? ')
input_distance = int(input_distance)

###
# query for search term
#
query_location_search = get_location_search_term(sqlcon = sqlite_conn, search = input_search)

###
# prepare column metadata, create dataframe, add `int_loc_within` defaulting to 0
#
query_location_search_list_column = list(map(lambda x: x[0], query_location_search.description))
df = pd.DataFrame(query_location_search, columns = query_location_search_list_column)
df['int_loc_within'] = 0

if len(df) == 0:
	print("No result for: " + input_search)
	sys.exit()

###
# main loop to calculate `int_loc_within` for each location
#
for main_index, main_row in df.iterrows():

	int_location_counter = 0

	# sub-loop to iterate over compared
	for comp_index, comp_row in df.iterrows():
		# check to make sure only consideration given to `locationid` of other trucks
		if main_row['permit'] != comp_row['permit']:
			# generate two points, calculate distance between them
			location_main = geopy.Point(main_row['Latitude'], main_row['Longitude'])
			location_comp = geopy.Point(comp_row['Latitude'], comp_row['Longitude'])

			dist = get_distance_feet(location_1 = location_main, location_2 = location_comp)

			# if distance is less than threshold, add to counter
			if dist < input_distance:
				int_location_counter = int_location_counter + 1

	# write counter back to df
	df.at[main_index, 'int_loc_within'] = int_location_counter

###
# sort and output
#
df_sorted = df.sort_values(by=['int_loc_within'], ascending=False)
df_sorted = df_sorted.head(3)

print("---")
print("Search: " + input_search)
print("Distance: " + str(input_distance) + " (feet)")
print("---")
for index, row in df_sorted.iterrows():
	print(row['Applicant'] + " / " + row['Address'] + ' / Nearby: ' + str(row['int_loc_within']))

###
# close sqlite
#
sqlite_conn.close()