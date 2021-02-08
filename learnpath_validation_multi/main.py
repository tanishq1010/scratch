import pandas as pd
from API_call_method import callAPI
import traceback
import os
import sys
import multiprocessing
import time

# from get_valid_goal_exams import *

df = pd.read_csv('mongo_data.csv')


def function(var):
    df1 = pd.DataFrame(
        columns=['ObjectId', 'Display_learnpath_name', 'Learnpath_name', 'Do_learnpaths_match', 'Question_code'])
    i = 0
    var11 = var
    # for ind in df.index:
    object_id = var11
    # print(object_id)
    url = f"/learning_objects/{object_id}?embed=true&next_status=true"
    response = callAPI('GET', 'https://knowledge-blue.embibe.com', url,
                       'a3e65d48-1c51-4191-96fb-1ee2d07d47da:7e02ba0f3c16a3f5231c51a42ffa76b84cf18480f74a02ca4c43ceb85b6ea8ba1f27564951cc70d49033d96334cdde23674939f05175339680ce3baabcb51ffd',
                       '{}')
    # print(response.json())
    try:
        content = response.json()['content']
        try:
            question_code = response.json()['question_code']
        except:
            question_code = 'question code key not available'
        for item in content:
            try:
                for item in content['question_meta_tags']:
                    try:
                        for item in item['learning_maps_data']:
                            try:
                                display_learnpath_name = item['display_learnpath_name']
                            except:
                                display_learnpath_name = 'display_learnpath_name key not present'
                            try:
                                learnpath_name = item['learnpath_name']
                            except:
                                learnpath_name = 'learnpath_name key not available'

                            if learnpath_name.lower() == display_learnpath_name.lower():
                                var = 'Yes'
                            else:
                                var = "No"
                            df1.loc[len(df1)] = [object_id, display_learnpath_name, learnpath_name, var, question_code]
                    except:
                        print(traceback.format_exc())
                        df1.loc[len(df1)] = [object_id, 'learning_maps_data key missing', 'Na', 'Na', question_code]
            except:
                print(traceback.format_exc())
                df1.loc[len(df1)] = [object_id, 'question_meta_tags key missing', 'Na', 'Na', question_code]
    except:
        print(traceback.format_exc())
        df1.loc[len(df1)] = [object_id, response.status_code, 'Na', 'Na', 'Na']
    # i += 1
    # if i > 4:
    #     break
    df1 = df1.loc[df1['Do_learnpaths_match'].str.contains('No')]
    # print(df1)
    if len(df1) > 0:
        df1.to_csv(f"Results/{var11}testing.csv", index=False)


processes = []
i = 0
j = 0
for ind in df.index:
    time.sleep(0.1)
    var = df['_id'][ind]
    p = multiprocessing.Process(target=function, args=(var,))
    processes.append(p)
    p.start()
    i += 1
    j += 1
    print(j)
    if i ==2000:
        print('2000')
    if i > 30000:
        print('BREAKING')
        break
    if j >= 200:
        j = 0
        for process in processes:
            process.join()
        processes = []
# for process in processes:
#     process.join()
