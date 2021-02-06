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
query["status"] = 'Published'

projection = {}
projection['_id'] = 0
projection['id'] = 1
projection['status'] = 1
df = pd.DataFrame(columns=['Status', 'Question_id'])
print('calling cursor')
cursor = collection.find(query, projection=projection)

print(cursor)
print('LOOP START')
df1 = pd.DataFrame(list(cursor))
# for doc in cursor:
# 
#     try:
#         status = doc['status']
#         question_code = doc['id']
#         # print(status,question_code)
# 
#         df.loc[len(df)] = [status, question_code]
# 
#     except:
#         print(traceback.format_exc())
df.to_csv('question_details.csv', index=False)
