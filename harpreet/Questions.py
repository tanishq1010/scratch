import pandas as pd
from pymongo import MongoClient
client = MongoClient("mongodb://ro_dsl:EHJpUwVO2vgMuk@10.141.11.78/contentgrail?authSource=contentgrail")
database = client["contentgrail"]
collection = database["learning_objects_versions"]
id_list = pd.read_csv('tbd.csv')['CG ID'].to_list()
query = {}
# id_list=[2293340]
query["status"] = {"$regex":".*UAT.*"}
query['id'] = {'$in':id_list}


projection = {}
projection["id"] = 1.0
projection["status"] = 1.0
projection["_id"] = 0.0
projection["updated_by"] = 1.0
projection["updated_at"] = 1.0
projection['content'] = 1.0

cursor = collection.find(query, projection = projection)

ids = []
for doc in cursor:
    question = {}
    question["id"] = doc['id']
    question["status"] = doc['status']
    question["updated_at"] = doc['updated_at']
    question["updated_by"] = doc['updated_by']
    
    try:
        bmt = doc['content']['book_meta-tags']
        
        for entry in bmt:
            if entry['key'] == 'Code':
                question['Bookcode'] = entry['value']
                if entry['key'] == 'Grade':
                    question['Grade'] = entry['value']
                    if entry['key'] == 'Subject':
                        question['Subject'] = entry['value']
    except:
        
        question['Bookcode'] = "No BMT"
        
    try:
        lm = []
        
        for entry in doc['content']['question_meta_tags']:
            lm.extend(entry['topics_learn_path_name'])
            
    except:
        pass
    
    question['lm']=lm
    ids.append(question)
                
final_df = pd.DataFrame(ids)
final_df.to_csv('Required Report.csv')