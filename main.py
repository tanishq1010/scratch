import pandas as pd
from pymongo import MongoClient
import  numpy as np
import multiprocessing

def conversion_to_id(df,int):
    k = 0
    df=pd.DataFrame(columns=['NQE_question_id'])
    df.to_csv(f"NQE_data_{int}.csv",index=False)
    df=pd.read_csv(f"NQE_data_{int}.csv")
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



        except Exception as e:
            print(e)
        k += 1
        print(k)

    df.to_csv(f"NQE_data_{int}.csv", index=False)




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
# df = pd.DataFrame(columns=['NQE_question_id'])
# df.to_csv('NQE_data.csv', index=False)
# df = pd.read_csv("NQE_data.csv")
# print(df)

df_split = np.array_split(df1, 4)





LIST=[df_split[0],df_split[1],df_split[2],df_split[3]]
LIST2=[1,2,3,4]


processes=[]
for i in range(len(LIST)):
    p = multiprocessing.Process(target=conversion_to_id, args=(LIST[i],LIST2[i]))
    processes.append(p)
    p.start()
    # conversion_to_id(LIST[i],LIST2[i])



df1=pd.read_csv('NQE_data_1.csv')
df2=pd.read_csv('NQE_data_2.csv')
df3=pd.read_csv('NQE_data_3.csv')
df4=pd.read_csv('NQE_data_4.csv')
df=pd.concat([df1,df2,df3,df4])
df.drop_duplicates(inplace=True)
df.to_csv('NQE_data.cav',index=False)





# for goal_exam in goal_exams:
#
#
#     # src.main(goal_exam[1],goal_exam[0])
#     p = multiprocessing.Process(target=src.main, args=(goal_exam[1], goal_exam[0],))
#     processes.append(p)
#     p.start()
#
# p = multiprocessing.Process(target=get_missing_books, args=("rr",))
# processes.append(p)
# p.start()

# LIST=
# for






# df1.reset_index(drop=True, inplace=True)




# conversion_to_id(df_split[0])
