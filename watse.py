import pandas as pd
from API_call_method import callAPI
import pandas as pd
from pymongo import MongoClient
import numpy as np

client = MongoClient(
    "mongodb://ro_dsl:EHJpUwVO2vgMuk@10.141.11.78/contentgrail?authSource=contentgrail&replicaSet=cg-mongo-prod&readPreference=secondaryPreferred")
# client = MongoClient("mongodb://10.143.1.95:27017/")
database = client["contentgrail"]
collection = database["learning_maps"]


query = {}
query["learnpath_name"] = {'$regex':'chhattisgarh board'}


projection = {}
projection["_id"] = 0
projection["learnpath_name"] = 1.0
projection["format_reference"] = 1.0

cursor = collection.find(query, projection=projection)
df1 = pd.DataFrame(list(cursor))
df1.to_csv('mongo_data.csv',index=False)


# df=pd.read_csv('mongo_data')
# for ind in df.index:
#     format_refrence=''
#     learnpath_name1=''
#     host='http://content-demo.embibe.com'
#     url="/learning_objects?where={'status':{'$in':['Published','Approved','draft','approved','UAT Approved']}}&lo_type=Video&lm_filter={%22format_reference%22:%22" + str(
#                         format_refrence) + "%22,%22learnpath_name%22:{%22$regex%22:%22" + str(
#                         learnpath_name1) + "%22}}&embed=true&max_results=100000",
#     response=callAPI('GET',host,url,'','{}')





