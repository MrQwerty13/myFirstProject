# section for importing some very important tools
import os
import random
from fastapi import FastAPI, Query
from pymongo import MongoClient
from pydantic import BaseModel


app = FastAPI()
mult = os.environ.get('MULTIPLIER', 1)
mongo_user = os.environ.get('MONGO_USER', 'root')
mongo_pass = os.environ.get('MONGO_PASS', 'password')
mongo_host = os.environ.get('MONGO_HOST', 'localhost')
mongo_port = os.environ.get('MONGO_PORT', '27017')
mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}?authSource=admin"
print(mongo_uri)
client = MongoClient(mongo_uri)
db = client['testapp']
collection = db['records']

class Record(BaseModel):
    id: str
    name: str
    value: int

"""
Generates and returns a random number within a specified range.

This endpoint accepts optional query parameters 'min' and 'max' to define the range for the random number generation.
If not provided, 'min' defaults to 1 and 'max' defaults to 100. Both parameters must be greater than or equal to 1.

Args:
    min (int, optional): The minimum value for the random number (inclusive). Defaults to 1. Must be >= 1.
    max (int, optional): The maximum value for the random number (inclusive). Defaults to 100. Must be >= 1.

Returns:
    dict: A dictionary containing the min, max, generated random number, and a descriptive message.
"""
@app.get('/')
def give_a_num(min: int = Query(1, ge=1), max: int = Query(100, ge=1)):
    """
    This function can swap max_int and min_int if max_int < min_int
    """
    if max > min:
        rand = random.randint(int(min), int(max)) * int(mult)
        return {
            'min': min,
            'max': max,
            'mult': mult,
            'rand': rand,
            'message': f"Here is a random number {rand} between {min} and {max}, multiplied by {mult}"
        }
    elif max < min:
        rand = random.randint(int(max), int(min)) * int(mult)
        return {
            'min': max,
            'max': min,
            'mult': mult,
            'rand': rand,
            'message': f"Here is a random number {rand} between {min} and {max}, multiplied by {mult}"
        }
    else:
        return 'I\'m sorry but it cannot be strated due to reason the min_int == max_int ;)'

@app.post("/addrecord")
def add_record(record: Record):
    collection.insert_one(record.dict())
    print(f"Added {record.dict()}")
    return {"message": f"Record {record.name} added successfully"}

@app.get('/getrecords')
def get_records():
    records = []
    for rec in collection.find({}):
        rec["_id"] = str(rec["_id"])     # <-- ключевая строка
        records.append(rec)
    print(records)
    return {
        'records': records,
        'message': 'Here are all the records in the database'
    }
