import sqlite3
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
from typing import Dict
import sys
import os

def read_sql_file(filename: str) -> str: 
    with open(filename, 'r') as file:
        return file.read()

def parse_jmdict_entities(filename: str) -> Dict[str, str]:
     dom = parse(filename)
     for element in dom.doctype.entities:
         print(element)

     return {}

if len(sys.argv) < 4:
    print("Usage: python jmdict_to_sql.py <database_schema> <jmdict_file> <database_name>") 
    exit()

database_schema = sys.argv[1]
jmdict_file = sys.argv[2]
database_name = sys.argv[3]

sql = read_sql_file(database_schema)
conn = sqlite3.connect(database_name)

cur = conn.cursor()
try:
    cur.executescript(sql)
except sqlite3.Error as err:
    print("Error creating tables")
    print(err)

    conn.close()
    os.remove(database_name)
    exit()

conn.commit()
cur.close()

parse_jmdict_entities(jmdict_file)

conn.close()
