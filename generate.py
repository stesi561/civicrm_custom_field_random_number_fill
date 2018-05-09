#! /usr/bin/env python

import MySQLdb
import sys
import csv


from random import *


base =  '0123456789'
length = range(10)
generated = set()


def generate():
    return "".join(choice(base) for x in length)



with open('setup.csv','r') as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        if len(row) < 2:
            continue
        if 'MYSQL_USER' in row[0]:            
            user = row[1]
        if 'MYSQL_PW' in row[0]:
            password = row[1]
        if 'MYSQL_DB' in row[0]:
            database = row[1]
        if 'MYSQL_TABLE' in row[0]:
            table = row[1]
        if 'MYSQL_COLUMN' in row[0]:
            column_name = row[1]


host = 'localhost'
conn = MySQLdb.connect(host, user, password, database)
    
cur = conn.cursor()
    

get_number_of_contacts = 'SELECT id FROM civicrm_contact'


cur.execute(get_number_of_contacts)
contacts = cur.fetchall()

output = []

for contact in contacts:
    cid = int(contact[0])
    
    candidate = generate()
    while candidate in generated:
        candidate = generate()

    generated.add(candidate)

    
    output.append((cid, candidate))
    ins_str = 'insert into {table_name} (entity_id, {column_name}) VALUES (%s, %s)'
    ins_str = ins_str.format(table_name = table,column_name = column_name)
    cur.execute(ins_str, (cid, candidate))


conn.commit()
cur.close()

