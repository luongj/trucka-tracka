#!/usr/bin/env python3
import pandas as pd
import sqlite3

###
# sqlite setup
#
file_sqlite3 = 'trucka-tracka.db'
sqlite_conn = sqlite3.connect(file_sqlite3)
sqlite_conn.row_factory = sqlite3.Row

###
# import statics
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



# 
if False:
	upload_csv_to_sqlite(sqlcon = sqlite_conn, file_csv = file_csv_mobile_food, db_table = db_table_mobile_food)

###
# close sqlite
#
sqlite_conn.close()