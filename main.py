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
df1 = pd.DataFrame(list(cursor))
df1.to_csv('mongo_data.csv',index=False)
df1 = pd.read_csv('mongo_data.csv')
print(df1)
df = pd.DataFrame(columns=['NQE_question_id'])
df.to_csv('NQE_data.csv', index=False)
df = pd.read_csv("NQE_data.csv")
print(df)
k = 0
for ind in df1.index:
    try:
        dict1 = eval(df1['questions'][ind])
        LIST = dict1['normal_questions']
        # print(LIST)
        # se = pd.Series(LIST)
        # df['NQE_question_id'] = se.values
        for i in range(len(LIST)):
            # print(LIST[i])
            df.loc[len(df)] = LIST[i]
        df.to_csv('NQE_data.csv', index=False)

    except Exception as e:
        print(e)
    k += 1
    print(k)

# df1.to_csv("trash.csv",index=False)








































# import pandas as pd
# from pymongo import MongoClient

# client = MongoClient("mongodb://10.141.12.55:27017/")
# database = client["learning_interventions"]
# collection = database["question_count"]

# # Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/


# query = {}
# query["lm_level"] = "chapter"

# projection = {}
# projection["_id"] = 0
# projection["questions.normal_questions"] = 1.0
# projection["lm_level_code"] = 1.0
# projection["concept_id"] = 1.0

# cursor = collection.find(query, projection=projection)
# df = pd.DataFrame(columns=['NQE_question_id'])
# df.to_csv('NQE_data.csv',index=False)
# i=0
# df = pd.read_csv("NQE_data.csv")
# for doc in cursor:
#  try:
    
#     # print(doc)
#     LIST = doc['questions']['normal_questions']
#     # print(LIST)
#     for question in LIST:
#         df.loc[len(df)] = [question]
#     if i%5000==0:
#      df.to_csv('NQE_data.csv', index=False)
#  except Exception as e:
#      print(e)
     
#  i+=1
#  print(i)

#     # print(df)

# # df = pd.DataFrame(list(cursor))
# # print(df)

# # print(get_question_meta_tag_CG('EM0000001-en',23))
