import pandas as pd
from pymongo import MongoClient
import numpy as np
import openpyxl
import traceback

uri = "mongodb://ro_content:EHJpUwVO2vgMuk@10.141.11.78/?authSource=contentgrail&authMechanism=SCRAM-SHA-256"
print('calling client')
client = MongoClient(uri)
database = client["contentgrail"]
collection = database["learning_objects"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/


query = {}
query["type"] = "Question"
query["status"] = "Published"
query["language"] = "en"

projection = {'_id': 1}

cursor = collection.find(query, projection=projection)
df1 = pd.DataFrame(list(cursor))
df1.to_csv('mongo_data.csv', index=False)
