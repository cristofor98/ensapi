import mysql.connector
from pymongo import MongoClient
import json
from bson import json_util


def connect_database(number_database):
    if number_database == 1:
        client = MongoClient('localhost', 27017)
    elif number_database == 2:
        mydb = mysql.connector.connect(
               host="localhost",
               user="api",
               password="yourpassword"
               )

def insert_base_value(number_database):
    if number_database == 1:
        database =  client.insurance_database
        collection = database["insurance"] 
        post_insurance_1 = {
            'id':100,
            'user_id': '1',
            'insurance': 'car insurance',
            'duration': '12000'
        }   
        post_insurance_2 = {
            'id':101,
            'user_id': '2',
            'insurance': 'pet insurance',
            'duration': '14000'
        }
        post_insurance_3 = {
            'id':102,
            'user_id': '3',
            'insurance': 'object insurance',
            'duration': '40000'
        }
        post_insurance_4 = {
            'id':103,
            'user_id': '4',
            'insurance': 'renters insurance',
            'duration': '20000'
        }
        insert_result = collection.insert_many([post_insurance_1, post_insurance_2, post_insurance_3, post_insurance_4])
        print('Multiple posts: {0}'.format(insert_result.inserted_ids))
    elif number_database == 2:
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE insurance_database")
        mycursor.execute("CREATE TABLE insurances (id INT,user_id INT, insurance VARCHAR(255),duration VARCHAR(255))")
        sql = "INSERT INTO insurances (id,user_id,insurance,duration ) VALUES (%i, %s, %s, %s)" 
        val = [(100,'1','car insurance','12000'),(101,'2','pet insurance','14000'),
        (102,'3','object insurance','40000'),(103,'4','renters insurance','20000')]
        mycursor.executemany(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")


def insert_insurance(number_database,insurance_id,user_id,insuance,duration):
    if number_database == 1:
        new_id = insurance_id
        new_user_id = user_id
        new_insurance = insurance
        new_duration = duration
        data_insert = {
              'id': new_id,
              'user_id': new_user_id,
              'insurance': new_insurance,
              'duration': new_duration
        }
        insert_result = collection.insert_one(data_insert)
    elif number_database ==2:    
        sql = "INSERT INTO insurances id,user_id,insurance,duration ) VALUES (%i, %s, %s, %s)"
        val = (new_id, new_user_id,new_insurance,new_duration)
        mycursor.execute(sql, val)


def search_by_user(number_database,user_id):
    if number_database == 1:
       new_user_id = str(user_id)
       query = {'user_id': new_user_id}
       print(query)
       find_results = list(collection.find(query)) 
       return find_results
    elif number_database ==2:
       sql = "SELECT * FROM insurance WHERE user_id = %s"
       mycursor.execute(sql,new_user_id)
       myresult = mycursor.fetchall()
       return myresult

def search_by_insurnaces(number_database,insurance_id):
    if number_database == 1:
        new_id = number
        print(new_id)
        print(type(new_id))
        find_results = list(collection.find({'id':new_id}))
        return find_results
    elif number_database ==2:
        sql = "SELECT * FROM insurance WHERE id = %d"
        mycursor.execute(sql,insurance_id)
        myresult = mycursor.fetchall()
        return myresult
