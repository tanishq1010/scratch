

import pandas as pd
from pymongo import MongoClient
import numpy as np
import traceback

client = MongoClient("mongodb://10.141.12.55:27017/")
database = client["learning_interventions"]
collection = database["question_count"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/


query = {}
query['lm_level']='chapter'

projection = {}
projection["_id"] = 0
projection["questions.normal_questions"] = 1.0

cursor = collection.find(query, projection=projection)
df1 = pd.DataFrame(list(cursor))

df1 = df1.applymap(str)

df2=pd.read_csv('OT_MB_questions_status_in_NQE.csv')
df2=df2.loc[df2['Present in NQE in published state'].str.contains('No')]
df2.insert(3, "Present in NQE", '')

i = 0

print('loop started')
for ind in df2.index:
    var = str(int(df2['question_id'][ind]))
    
    df_new = df1.loc[df1['questions'].str.contains(var)]
    if len(df_new) > 0:
        df2['Present in NQE'][ind] = 'Yes'
    else:
        df2['Present in NQE'][ind] = 'No'
    i += 1
    if i > 100:
        break
df2.to_csv('testing.csv',index=False)


