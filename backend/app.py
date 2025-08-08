from flask import Flask, request
import json
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

filename = 'backend_file.txt'

load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')

try: 
    client = MongoClient(mongodb_uri, ServerSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("MongoDB connection successful")
except ConnectionFailure as e:
    print("MongoDB connection failed:", e)
    
db = client["flask_mongodb"]
user_collection = db["user"]

app = Flask(__name__)

st_details = {
    "id": 11382,
    "name": "Jitu Rajput",
    "father_name": "Prahlad Rajput",
    "class": "9 C",
    "roll_no": 23,
    "address": "51 chaat street, Indore, M.P.",
    "email": "jiturajput4456@email.com",
    "phone": "123456789"
}

# This function writes data to a backend file
def write_to_file():
    with open(filename, 'w') as file:
        file.write("car, motorcycle, bus, truck, aeroplane, train, bicycle")

# This function  reads data from file 
def read_from_file():
    with open(filename, 'r') as file:
        content = file.read()
        
    content_list = content.split(", ")
    # split the returned string into a python list 
    return content_list

def write_to_json(data):
    with open('new_file.json', 'w') as file:
        json.dump(data, file)
        
def read_from_json():
    with open('new_file.json', 'r') as file:
        content = json.load(file)
        
    return content
        
@app.route('/api')
def get_json_data():
    write_to_json(st_details)
    data = read_from_json()
    if not data:
        return {"error": "data not found"}, 404
    return data

@app.route('/api2')
def get_info():
    write_to_file()
    content_list = read_from_file()
    my_list = json.dumps(content_list)
    # convert the python list into a json format 
    return my_list

@app.route('/submit', methods=['POST'])
def submit():
    json_data = request.get_json()      
    # get json data from the request if it exists
    if json_data:
        data = json.loads(json_data)    # parse the json data to python dict
        user_collection.insert_one(data)     # insert the data into the MongoDB user_collection
        return {"status_code": 200}
    else:
        return {"status_code": 400}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)