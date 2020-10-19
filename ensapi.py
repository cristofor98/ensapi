from pymongo import MongoClient
from flask import Flask, Response
from flask import jsonify, request
import json
from bson import json_util
import random
import time
import adapter

client = MongoClient('localhost', 27017)
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

#find
numid = 2
myquery = {"user_id": "12" }
results = database.collection.find(myquery)
for result in results:
  print(result)


#create
user_id = 4
insurance_name = 'renters insurance'
duration = '2'
myquery_insert = {
    'user_id': user_id,
    'insurance': insurance_name,
    'duration': duration
}
insert_result = collection.insert_one(myquery_insert)
print('One post: {0}'.format(insert_result.inserted_id))
 
#typeofinsurance
type_results = collection.distinct("insurance")
print(type_results)

def set_timer(value,t): 
    global time_dictionary
    initial_time = time.time()
    time_dictionary[value] = initial_time
    print(time_dictionary[value])
    global timer
    timer = t


def check_time(value):
    global time_dictionary
    global timer
    print(time_dictionary)
    print("checktime")
    print(time_dictionary.get(value))
    if time_dictionary.get(value) != 0:
        print("ccccccc")
        print(timer)
        duration = time.time() - time_dictionary.get(value)
        print(duration)
        if int(duration) > timer:
           print("aaaa")
           time_dictionary[value] = 0
           global insurance_dictionary
           global duration_dictionary
           global user_id_dictionary
           global id_dictionary
           del insurance_dictionary[value]
           del duration_dictionary[value]
           del user_id_dictionary[value]
           del id_dictionary[value]
           return True
        else:
           print("bbbbb")
           return False


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/insurance', methods = ['GET'])
def type_of_insurance():
    if request.method == 'GET':
        type_results = collection.distinct("insurance")
        return jsonify({'result': type_results})

@app.route('/insurance/create', methods = ['POST'])
def start_task():
  global LIMIT
  global counter
  global top_counter
  global top_dictionary
  priority = request.args.get('priority')
  print(priority)
  if priority == 'top':
    if counter == LIMIT: 
       response = {'message': 'no resources are available for task please wait'} 
       return jsonify(response), 404
    else:
        counter = counter + 1
        top_counter = top_counter + 1
        print(counter)
  else:           
    if counter == LIMIT-1:
        response = {'message': 'no resources are available for task please wait'} 
        return jsonify(response), 404
    else:
        counter = counter + 1
        print(counter)
  random_id = random.randint(1,10)
  global id_dictionary
  while random_id in id_dictionary.values():
    random_id = random.randint(1,10)
  id_dictionary[random_id] = random_id
  print(id_dictionary)
  new_user_id = request.values.get('user_id')
  global user_id_dictionary
  user_id_dictionary[random_id] = new_user_id
  if top_counter == 1:
     top_dictionary['top'] = random_id 
  seconds = 300  
  set_timer(random_id,seconds)
  response = {'link_id': random_id,'status':'buiding','time':seconds} 
  return jsonify(response), 200

@app.route('/insurance/create/<int:value>', methods = ['PATCH', 'GET'])
def insert_data(value):
    if request.method == 'PATCH':
      global id_dictionary
      if value in id_dictionary.values():
        if check_time(value) == True:
          print("aaaa")
          answer = {'error':'time for this task expired'}
          return  jsonify(answer), 408
        global insurance_dictionary
        new_insurance = request.values.get('insurance')
        insurance_dictionary[value] = new_insurance
        response = {'link_id': value,'status':'building'}
        print(new_insurance)
        return jsonify(response), 200
      else:
        answer = {'error':'this id route is not correct, write the correct'}
        return  jsonify(answer), 404
    elif request.method == 'GET':
        print(value)
        if value in id_dictionary.values():
            print(" value este")
            if check_time(value) == True :
                answer = {'error':'time for this task expired'}
                return  jsonify(answer), 408
            else:   
                print(id_dictionary)
                new_user_id = user_id_dictionary.get(value)
                print(new_user_id)
                find_results = list(collection.find({'user_id':new_user_id}))
                global top_dictionary
                global top_counter
                if value in top_dictionary.values():
                    top_counter = top_counter - 1
                global counter
                counter = counter - 1
                print(counter)
                print(id_dictionary[value])
                del user_id_dictionary[value]
                del id_dictionary[value]
                if find_results:
                    for user in find_results:
                        user["_id"] = str(user["_id"])
                    print(find_results)
                    return Response(
                        response = json.dumps({'link_id': value,'status':'done', 'result': find_results}),
                        status = 201 
                        )
                else:
                    return Response(
                        response = json.dumps({'error': 'cannot find user'}),
                        status = 500 
                        )
        else:
            answer = {'error':'this id route is not correct, write the correct'}
            return  jsonify(answer), 404     

@app.route('/insurance/create/<int:value>/duration', methods = ['PATCH'])
def insert_duration(value):
   if request.method == 'PATCH':
      global id_dictionary
      if value in id_dictionary.values():
        if check_time(value) == True:
          answer = {'error':'time for this task expired'}
          return  jsonify(answer), 408
        global duration_dictionary
        new_duration = request.values.get('duration')
        print("duration", new_duration)
        duration_dictionary[value] = new_duration
        print(duration_dictionary[value])
        response = {'link_id': value,'status':'building'}
        return jsonify(response), 200
      else:
        answer = {'error':'this id route is not correct, write the correct'}
        return  jsonify(answer), 404

@app.route('/insurance/create/<int:value>/finalize', methods = ['PUT'])
def insert_value_in_database(value):
   if request.method == 'PUT':
      global id_dictionary
      if value in id_dictionary.values():
        if  check_time(value) == True:
          answer = {'error':'time for this task expired'}
          return  jsonify(answer), 408
        global duration_dictionary
        global insurance_dictionary
        global user_id_dictionary
        new_user_id = user_id_dictionary.get(value)
        new_duration = duration_dictionary.get(value)
        new_insurance = insurance_dictionary.get(value)
        global last_id
        new_id = last_id + 1
        last_id = new_id
        data_insert = {
              'id': new_id,
              'user_id': new_user_id,
              'insurance': new_insurance,
              'duration': new_duration
        }
        insert_result = collection.insert_one(data_insert)
        print(new_id)
        print(data_insert)
        print("aaaaaaaaaaaaaa")
        print(insert_result)
        print(insert_result.inserted_id)
        del insurance_dictionary[value]
        del duration_dictionary[value]
        response = {'link_id': value,'status':'processing'}
        return jsonify(response), 200
      else:
        answer = {'error':'this id route is not correct, write the correct'}
        return  jsonify(answer), 404

@app.route('/insurance/<int:number>')
def find_insurance_by_id(number):
    new_id = number
    print(new_id)
    print(type(new_id))
    find_results = list(collection.find({'id':new_id}))
    if find_results:
      for user in find_results:
        user["_id"] = str(user["_id"])
      return Response(
        response = json.dumps(find_results),
        status = 200
      )
    else:
      return Response(
        response = json.dumps({'erro':'cannot find insurance'}),
        status= 500
      )

@app.route('/user/<int:number>/insurances')
def user_insurence(number):
    new_user_id = str(number)
    print(number)
    query = {'user_id': new_user_id}
    print(query)
    find_results = list(collection.find(query))
    print(find_results)
    if find_results:
        for user in find_results:
            user["_id"] = str(user["_id"])
        return Response(
            response = json.dumps(find_results),
            status = 200 
        )
    else:
        return Response(
            response = json.dumps({'error': 'cannot find user'}),
            status = 500 
        )
 

@app.route('/working')
def tasks_that_are_working():
  global counter
  return Response(
          response = json.dumps({'working': counter}),
          status = 200 
        )


if __name__ == '__main__':
     time_dictionary = {}
     top_dictionary = {}
     random_id = 0
     counter = 0
     top_counter = 0
     LIMIT = 5
     timer = 0
     last_id = 103
     id_dictionary = {}
     user_id_dictionary = {}
     insurance_dictionary = {}
     duration_dictionary = {}
     app.run()



