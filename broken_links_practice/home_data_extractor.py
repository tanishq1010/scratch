import requests
import pandas as pd
import json
from openpyxl import Workbook, load_workbook
# from miscellaneous import *
from subject_data_extractor import subject_data_extractor
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

    def main(self, child_id, board, grade, exam, goal, embibe_token):
        payload = {
            "board": goal,
            "child_id": child_id,
            "exam": exam,
            "exam_name": exam,
            "goal": goal,
            "grade": grade,
            "fetch_all_content":True
        }


        response1=callAPI('POST','https://preprodms.embibe.com','/fiber_ms/v1/home/practise',embibe_token,json.dumps(payload))
        # response1 = self.callAPI(
        #     f"/fiber_ms/v1/home",
        #     json.dumps(payload),
        #     'POST', embibe_token)



        # df_positive_results_all_subjects = pd.read_csv("positive_learn_results_all_subjects.csv")
        # df_negative_results_all_subjects = pd.read_csv("negative_learn_results_all_subjects.csv")



        df_positive_results = pd.read_csv("positive_learn_results.csv")
        df_negative_results = pd.read_csv("negative_learn_results.csv")
        try:
            for item in response1.json():
                home_data = [child_id, exam, goal,grade]


                if item["content_section_type"] == "SUBJECTS":
                    for data in item["content"]:
                        if data["subject"] == "All Subjects":
                            continue
                        else:
                           try:
                               subject_data_extractor(child_id, board, grade, exam, goal, embibe_token, data["subject"],
                                                   home_data, df_negative_results, df_positive_results)
                           except Exception as e:
                               print(e)




                if (item["contentType"] == "chapter"):
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
                            format_refrence = data["learnmap_id"]
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
                            learnpath_name = data["learnpath_name"]
                        except:
                            learnpath_name=None
                        LIST = []
                        LIST = learnpath_name.split('--')
                        chapter = (LIST[len(LIST) - 1])
                        learnmap_id = data["learnmap_id"]
                        
                        
                        df_positive_results.loc[len(df_positive_results)] = home_data +  [title, Type, format_refrence, section_name,"All Subjects", subject_tagged,learnpath_name,learnmap_id,chapter]
                        df_positive_results.to_csv("positive_learn_results.csv", index=False)
        except:
            df_positive_results.loc[len(df_positive_results)] = home_data +  [response1.json(), '', '', '',"All Subjects", '','','','']
            df_positive_results.to_csv("positive_learn_results.csv", index=False)





def home_data(child_id, board, grade, exam, goal, embibe_token):
    src = Source()
    src.main(child_id, board, grade, exam, goal, embibe_token)


# home_data("", "", "", "", "",
#           "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTEwLTE1IDE3OjQyOjI2IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM2MTU1OTQsImVtYWlsIjoiYzEzNDEzOGUwNDc1QGppby1lbWJpYmUuY29tIn0.lG7sauHJW1Hwj3nQGzDBrBjyPbhaFJGGnZ05bbflJjkD-tmybjJ8V-Si7phyv6Wai28twrgH-J82P0iF7r_Sag")
