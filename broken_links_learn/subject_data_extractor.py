import requests
import pandas as pd
import json
from openpyxl import Workbook, load_workbook
# from miscellaneous import *
from API_call_method import callAPI


class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        self.host = 'https://preprodms.embibe.com'

    def callAPI(self, url, payload, method, token):
        self.headers['embibe-token'] = token
        response = requests.request(method, self.host + url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def main(self, child_id, board, grade, exam, goal, embibe_token, subject, home_data, df_negative_results,
             df_positive_results):
        payload = {
            "board": goal,
            "child_id": child_id,
            "exam": exam,
            "exam_name": exam,
            "goal": goal,
            "grade": grade,
            "onlyPractise": "false"
        }
        response1=callAPI('POST','https://preprodms.embibe.com',f"/fiber_ms/v1/home/{subject}",embibe_token,json.dumps(payload))
        # response1 = self.callAPI(
        #     f"/fiber_ms/v1/home/{subject}",
        #     json.dumps(payload),
        #     'POST', embibe_token)
        try:
            for item in response1.json():
               
                
                 if item["contentType"] == "learn_chapter":
                    try:
                        section_name = item["section_name"]
                    except:
                        section_name=None
                    for data in item["content"]:
                        try:
                            title = data["title"]
                        except:
                            title=None
                        try:
                            description = data["description"]
                        except:
                            description=None
                        try:
                            format_refrence=data["learnmap_id"]
                        except:
                            format_refrence=None
                        a_string = format_refrence
                        split_string = a_string.split("/", 1)
                        format_refrence = split_string[0]
                        try:
                            Type = data["type"]
                        except:
                            Type=None
                        try:
                            subject_tagged = data["subject"]
                        except:
                            subject_tagged=None
                        try:
                            learnpath_name=data["learnpath_name"]
                        except:
                            learnpath_name=None
                        LIST = []
                        LIST = learnpath_name.split('--')
                        chapter=(LIST[len(LIST)-1])
                        learnmap_id=data["learnmap_id"]
                        
                        
                        df_positive_results.loc[len(df_positive_results)] = home_data + [title, Type, format_refrence,section_name, subject,subject_tagged,learnpath_name,learnmap_id,chapter]
                        df_positive_results.to_csv("positive_learn_results.csv", index=False)
        except:
            df_positive_results.loc[len(df_positive_results)] = home_data + [response1.json(), '', '','', subject,'','','','']
            df_positive_results.to_csv("positive_learn_results.csv", index=False)


        # df11 = pd.read_csv("positive_learn_results.csv")
        # df2 = pd.read_csv("positive_learn_results.csv")

        # df1 = df11[df11['Exam'].str.contains(exam)]
        # df2 = df1[df1['Exam'].str.contains(exam)]

        # for ind in df2.index:
        #     df_new = df1.loc[df1['Id'] == df2["Id"][ind]]
        #     if len(df_new)>0:
        #        df_new1=df_new.loc[df_new["Section_name"]==df2["Section_name"][ind]]
        #        if len(df_new1) == 1:
        #             df2["present only once"][ind] = str("yes")
        #        else:
        #             df2["present only once"][ind] = str("no")


        # df=pd.concat([df11,df2])

        # df = df.dropna(axis=0, subset=['present only once'])
        # df.to_csv('positive_learn_results.csv', index=False)



def subject_data_extractor(child_id, board, grade, exam, goal, embibe_token, subject, home_data, df_negative_results,
                           df_positive_results):
    src = Source()
    src.main(child_id, board, grade, exam, goal, embibe_token, subject, home_data, df_negative_results,
             df_positive_results)

# subject_data_extractor("", "", "", "", "",
#                        "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTEwLTE1IDE3OjQyOjI2IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM2MTU1OTQsImVtYWlsIjoiYzEzNDEzOGUwNDc1QGppby1lbWJpYmUuY29tIn0.lG7sauHJW1Hwj3nQGzDBrBjyPbhaFJGGnZ05bbflJjkD-tmybjJ8V-Si7phyv6Wai28twrgH-J82P0iF7r_Sag",
#                        "Science")
