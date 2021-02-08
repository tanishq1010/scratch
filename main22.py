import pandas as pd
from pymongo import MongoClient
import numpy as np
import traceback

client = MongoClient("mongodb://10.141.12.55:27017/")
database = client["learning_interventions"]
collection = database["question_count"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/


query = {}

projection = {}
projection["_id"] = 0
projection["questions.normal_questions"] = 1.0

cursor = collection.find(query, projection=projection)
var = list(cursor)
#print(var)

var = list(cursor)
# print(var)
LIST_app = []
for doc in var:
    try:
        LIST = doc['questions']['normal_questions']
        # print(LIST)
        LIST_app = LIST_app + LIST
    except:
        print(traceback.format_exc())

df = pd.DataFrame(data=LIST_app, columns=['id'])

df.to_csv('mongo_data.csv', index=False)

