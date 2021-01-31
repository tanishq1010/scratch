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

projection = {}
projection['_id'] = 0
projection['question_code'] = 1
projection['content'] = 1
df = pd.DataFrame(columns=['Question_code', 'Question_text', 'Exam', 'Subject', 'Unit', 'Chapter', 'learning maps'])
print('calling cursor')
cursor = collection.find(query, projection=projection)
df111 = pd.DataFrame(list(cursor))
df111.to_csv('mongo_data.csv', index=False)
print(cursor)
print('LOOP START')
for doc in cursor:

    try:
        LIST = []
        question_code = doc['question_code']
        # print(question_code)
        question_text = doc['content']['question_details']['en']['question_txt']
        var1 = None
        var2 = None

        for ch in question_text:
            if 2305 < ord(ch) < 2416:
                var1 = question_code
                var2 = question_text
                # print(var1, var2)
                break
        if var1 is not None and var2 is not None:
            try:
                exam = doc['content']['question_meta_tags'][0]['exams']
            except:
                exam = None
            try:
                subject = doc['content']['question_meta_tags'][0]['subject']
            except:
                subject = None
            try:
                unit = doc['content']['question_meta_tags'][0]['unit']
            except:
                unit = None
            try:
                chapter = doc['content']['question_meta_tags'][0]['chapter']
            except:
                chapter = None
            # print(exam, subject, unit, chapter)

            for item in doc['content']['question_meta_tags']:
                try:
                    learning_maps = item['learning_maps']
                except:
                    learning_maps = None
                LIST.append(learning_maps)

            # print(LIST)
            df.loc[len(df)] = [var1, var2, exam, subject, unit, chapter, LIST]
        else:
            continue
    except:
        print(traceback.format_exc())
df.to_csv('question_details.csv',index=False)

# df1 = pd.DataFrame(list(cursor))
# df1.to_csv('mongo_data.csv', index=False)
# df1 = pd.read_csv('mongo_data.csv')
# # df1.to_csv("trash.csv",index=False)
# df_results = pd.DataFrame(columns=['Question_code', 'Question_text'])
#
# for ind in df1.index:
#     question_text = str(df1['content'][ind])
#     question_code = df1['question_code'][ind]
#     for ch in question_text:
#         if 2305 < ord(ch) < 2416:
#             # if question_code == "EM0000001-en":
#             #     print(ch)
#             #     print(ord(ch))
#             df_results.loc[len(df_results)] = [df1['question_code'][ind], question_text]
#             break
# df_results.to_excel('Hindi_questions_appearing_in_english.xlsx', index=False)
