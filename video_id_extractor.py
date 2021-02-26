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
df=pd.read_csv('Video Id.csv')
LIST=df['VIdeo Id'].to_list()
query = {}
query["id"] = {'$in':LIST}


projection = {'_id': 0,'id':1,'content.question_meta_tags.learning_maps':1}


cursor = collection.find(query, projection=projection)
questions = []
for doc in cursor:
    id=doc['id']
    _lms = []
    for item in doc['content']['question_meta_tags']:
        for lms in item.get('learning_maps',[]):
            _lms.extend(lms)
    
    question_meta = {'id':id,'lms':_lms}
    questions.append(question_meta)

df = pd.DataFrame(questions)
df.to_csv('mong-_data.csv',index=False)
    
    

# df1 = pd.DataFrame(list(cursor))
df1.to_csv('mongo_data.csv', index=False)
