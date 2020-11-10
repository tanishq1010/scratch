import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://10.141.12.55:27017/")
database = client["learning_interventions"]
collection = database["question_count"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/


query = {}
query["lm_level"] = "chapter"

projection = {}
projection["_id"] = 0
projection["questions.normal_questions"] = 1.0
projection["lm_level_code"] = 1.0
projection["concept_id"] = 1.0

cursor = collection.find(query, projection=projection)
df = pd.DataFrame(columns=['NQE_question_id'])
df.to_csv('NQE_data.csv',index=False)
i=0
for doc in cursor:
 try:
    df = pd.read_csv("NQE_data.csv")
    # print(doc)
    LIST = doc['questions']['normal_questions']
    # print(LIST)
    for question in LIST:
        df.loc[len(df)] = [question]

    df.to_csv('NQE_data.csv', index=False)
 except Exception as e:
     print(e)
     
 i+=1
 print(i)

    # print(df)

# df = pd.DataFrame(list(cursor))
# print(df)

# print(get_question_meta_tag_CG('EM0000001-en',23))
