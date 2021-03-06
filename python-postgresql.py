#!/bin/python3

import json
import requests
import psycopg2
from datetime import datetime as dt
#from psycopg2 import connect

conn = psycopg2.connect(database="postgres", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")

cursor = conn.cursor()

url = 'https://health.data.ny.gov/api/views/xdss-u53e/rows.json?accessType=DOWNLOAD'
r = requests.get(url)
total = r.json()
county_list =[]
for list_row in total['data']:
    county_list.append(list_row[9])
counties_list = (set(county_list))
for county in counties_list:
    if '.' in county:
    	county=county.replace('.','_')
    if ' ' in county:
    	county=county.replace(' ','')
    cursor.execute("CREATE TABLE if not exists "+ county +" (test_date varchar, new_positivies int, cumulative_no_of_positives int, total_no_of_tests_performed int,cumulative_no_of_tests_performed int,Load_date date);");
for row in total['data']:
    date = dt.strptime(row[8], "%Y-%m-%dT%H:%M:%S")
    new_format = "%Y-%m-%d"
    date1 =date.strftime(new_format)
    county1 = row[9]
    if '.' in county1:
        county1=county1.replace('.','_')
    if ' ' in county1:
        county1=county1.replace(' ','')
    cursor.execute("Insert into "+county1+" (test_date,new_positivies,cumulative_no_of_positives,total_no_of_tests_performed,cumulative_no_of_tests_performed,Load_date) values(cast("+date1+" as varchar),"+row[10]+","+row[11]+","+row[12]+","+row[13]+",current_timestamp);");

for county in counties_list:
    if '.' in county:
        county=county.replace('.','_')
    if ' ' in county:
        county=county.replace(' ','')
    cursor.execute("SELECT * from "+ county +"");
    rows = cursor.fetchall();
    for row in rows:
        print ("test_date = ", row[0],row[1],row[2],row[3],row[4],row[5]);

cursor.close()
conn.close()


