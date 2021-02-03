import requests
import pandas as pd
import json
import random
from openpyxl import Workbook, load_workbook
from miscellaneous import *
from subject_data_extractor import subject_data_extractor



class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        self.host = 'https://fiberdemoms.embibe.com'

    def callAPI(self, url, payload, method, token):
        self.headers['embibe-token'] = token
        response = requests.request(method, self.host + url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def callAPI2(self, url, payload, method, token):
        self.headers['Authorization'] = token
        response = requests.request(method,  url, headers=self.headers, data=payload)
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
            "fetch_all_content": "true"
        }
        home_data = {'CBSE':'5ec5867a0c88fe5860961943','Jammu and Kashmir Board':'5faec359329f1db7f7a357f5','ICSE':'5eef299c420f624a7cd798db',
    'Maharashtra Board':'5ef30dcce52bc182d359ccfd','Karnataka Board':'5f12c93e7f10acd6461e5080','Telangana Board':'5f12c9997f10acd6461e50e9',
    'Rajasthan Board':'5ef2ff88e52bc182d359b8f7','Engineering':'5f17102be61885046e5d9780','Medical':'5f17177ee61885046e5db8d0',
            'Banking':'5ec586770c88fe586096193e','Insurance':'5f520569429ee9ee0e8c1b04','Railways':'5f52048858ae126dab8a36cd',
            'SSC':'5f5207e158ae126dab8a370e','Teaching':'5eb7ced0c20bf39d163d763c','Defence':'5f5206b031562a10f6a592ff','Tamil Nadu Board':'5f0602449a10ea4cb3b91bbd','National Recruitment Agency':'5fce2026c240c4991ec5e96a','Kerala Board':'5ff410033bb906d8743ba6f0'}
        # home_data={'CBSE':'5ec5867a0c88fe5860961943','Engineering':'5f17102be61885046e5d9780','Banking':'5ec586770c88fe586096193e','Medical':'5f17177ee61885046e5db8d0','Insurance':'5f520569429ee9ee0e8c1b04','Defence':'5f5206b031562a10f6a592ff','SSC':'5f5207e158ae126dab8a370e','Railways':'5f52048858ae126dab8a36cd','Teaching':'5eb7ced0c20bf39d163d763c'}
        

        response1 = self.callAPI(
            f"/fiber_ms/v1/home",
            json.dumps(payload),
            'POST', embibe_token)
        response2=self.callAPI2("https://content-demo.embibe.com/fiber_app/learning_maps/filters/"+str(home_data[goal])+"/"+str(goal)+"/"+str(exam),'{}','GET','048f38be-1b07-4b21-8f24-eac727dce217:gSEkC3dqDcIv1bbOk78UD9owjn7ins8D')
        LIST=[]
        for item in response2.json()["Subject"]:
            subject=item["name"]
            LIST.append(subject)
        
        LIST.sort()
        # print(LIST)
        LIST2=[]
        for item in response1.json():
             if item["content_section_type"] == "SUBJECTS":
              for data in item["content"]:
                if data["subject"] == "All Subjects":
                    continue
                else:
                    LIST2.append(data['subject'])
        
        LIST2.sort()
        # print(LIST2)
        all_subjects_present=False
        if LIST==LIST2:
            all_subjects_present=True

        count=0
        book_count=0
        embibe_explainers_count=0
        learn_count=0
        enrich_count=0
        for item in response1.json():
         
         explainer='EMBIBEEXPLAINERSVIDEOS'
         books='BOOKS'
         learn='EMBIBESYLLABUSLEARN' 
         enrich='ENRICHYOURLEARNING'
         if item['content_section_type']=="SUBJECTS":
            for data in item["content"]:
                count+=1
         if item['content_section_type'].find(explainer)==0:
            embibe_explainers_count+=1
         if item['content_section_type'].find(books)==0:
            book_count+=1
         if item['content_section_type'].find(learn)==0:
            learn_count+=1
         if item['content_section_type'].find(enrich)==0:
            enrich_count+=1
        # print(count,embibe_explainers_count,book_count,learn_count,enrich_count)




        df_positive_results_all_subjects = pd.read_csv("positive_learn_results_all_subjects.csv")
        df_negative_results_all_subjects = pd.read_csv("negative_learn_results_all_subjects.csv")



        df_positive_results = pd.read_csv("positive_learn_results.csv")
        df_negative_results = pd.read_csv("negative_learn_results.csv")

        for item in response1.json():
            home_data = [child_id, exam, goal,grade]
            if item["content_section_type"] == "HEROBANNER":
                hero_banner_checker(response1.json(), df_negative_results_all_subjects,
                                    df_positive_results_all_subjects, "negative_learn_results_all_subjects.csv",
                                    "positive_learn_results_all_subjects.csv", home_data, "All Subjects")


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


            if (item["content_section_type"] != "HEROBANNER" and item["content_section_type"] != "CONTINUELEARNING" and item["content_section_type"] != "SUBJECTS" and item[
                "content_section_type"] != "CONTINUELEARNING") and (
                    item["contentType"] != "Ad_banner" and item["contentType"] != "learn_chapter"and item["section_name"] != "Embibe Explainers"and item["section_name"] != "Books With Videos & Solutions"):
                section_name = item["section_name"]
                for data in item["content"]:
                    title = data["title"]
                    description = data["description"]
                    length = data["length"]
                    currency = int(data["currency"])
                    id = data["id"]
                    a_string = id
                    split_string = a_string.split("/", 1)
                    id= split_string[0]
                    Type = data["type"]
                    subject_tagged = data["subject"]
                    if description=="":
                        description=False
                    else:
                        description=True
                    if title == ""  or length == "" or length == 0 or currency < 0 or id == "" or Type == "":
                        length=minutes_converter(length)
                        df_negative_results_all_subjects.loc[len(df_negative_results_all_subjects)] = home_data + [length, Type, id, title,section_name,currency,"All Subjects", subject_tagged,"","","","","","",description]
                        df_negative_results_all_subjects.to_csv("negative_learn_results_all_subjects.csv", index=False)
                    else:
                        length=minutes_converter(length)
                        df_positive_results_all_subjects.loc[len(df_positive_results_all_subjects)] = home_data + [length, Type, id, title,section_name,currency,"All Subjects", subject_tagged,"","","","","","",description]
                        df_positive_results_all_subjects.to_csv("positive_learn_results_all_subjects.csv", index=False)

            if (item["contentType"] == "learn_chapter"):
                section_name = item["section_name"]
                for data in item["content"]:
                    title = data["title"]
                    description = data["description"]
                    # length = datta["duration"]
                    # currency = int(data["embium_coins"])
                    id = data["id"]
                    a_string = id
                    split_string = a_string.split("/", 1)
                    id= split_string[0]

                    Type = data["type"]
                    subject_tagged = data["subject"]
                    if description=="":
                        description=False
                    else:
                        description=True
                    if title == "" or id == "" or Type == "":
                        df_negative_results_all_subjects.loc[len(df_negative_results_all_subjects)] = home_data + ["", Type, id, title,section_name,"","All Subjects", subject_tagged,"","","","","","",description]
                        df_negative_results_all_subjects.to_csv("negative_learn_results_all_subjects.csv", index=False)
                    else:
                        df_positive_results_all_subjects.loc[len(df_positive_results_all_subjects)] = home_data + ["", Type, id, title,section_name,"","All Subjects", subject_tagged,"","","","","","",description]
                        df_positive_results_all_subjects.to_csv("positive_learn_results_all_subjects.csv", index=False)

        home_data = [child_id, exam, goal,grade]


        Embibe_Explainers = False
        if count==embibe_explainers_count:
                Embibe_Explainers = True
                # print(Embibe_Explainers)
                # break
        Books = False
        if count == book_count:
                Books = True
                # break
        Learn = False
        if count-1==learn_count:
                Learn = True
                # break
        Enrich_learning = False
        if count-1==enrich_count:
                Enrich_learning = True
                # break




    

        # df_positive_results = pd.read_csv("positive_learn_results.csv")
        if Embibe_Explainers == True and Books == True and Learn == True and Enrich_learning == True:
            df_positive_results_all_subjects.loc[len(df_positive_results_all_subjects)] = home_data + ["", "", random.randint(0, 1000000), "",
                                                                                         "All carousals present", "", "",
                                                                                         "All subject", "", "", Embibe_Explainers, Books,
                                                                                         Learn, Enrich_learning,""]

            df_positive_results_all_subjects.to_csv("positive_learn_results_all_subjects.csv", index=False)
        else:
            df_negative_results_all_subjects.loc[len(df_negative_results_all_subjects)] = home_data + ["", "", random.randint(0, 1000000), "",
                                                                                         "All carousals present", "", "",
                                                                                         "All subject", "", "", Embibe_Explainers, Books,
                                                                                         Learn, Enrich_learning,""]

            df_negative_results_all_subjects.to_csv("negative_learn_results_all_subjects.csv", index=False)
        if all_subjects_present==True:
            df_positive_results_all_subjects.loc[len(df_positive_results_all_subjects)] = home_data + ["", "", random.randint(0, 1000000), "",
                                                                                         "All subjet Tags present", "", "",
                                                                                         "All subjet Tags present", "yes all subjects are present in UI", "","", "",
                                                                                         "", "",""]

            df_positive_results_all_subjects.to_csv("positive_learn_results_all_subjects.csv", index=False)
        else:
            df_negative_results_all_subjects.loc[len(df_negative_results_all_subjects)] = home_data + ["", "", random.randint(0, 1000000), "",
                                                                                         "All subjet Tags present", "", "",
                                                                                         "All subjet Tags present", "no all subjects are not present in UI", "", "", "",
                                                                                         "", "",""]

            df_negative_results_all_subjects.to_csv("negative_learn_results_all_subjects.csv", index=False)





def home_data(child_id, board, grade, exam, goal, embibe_token):
    src = Source()
    src.main(child_id, board, grade, exam, goal, embibe_token)


# home_data("", "", "", "", "",
#           "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTEwLTE1IDE3OjQyOjI2IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM2MTU1OTQsImVtYWlsIjoiYzEzNDEzOGUwNDc1QGppby1lbWJpYmUuY29tIn0.lG7sauHJW1Hwj3nQGzDBrBjyPbhaFJGGnZ05bbflJjkD-tmybjJ8V-Si7phyv6Wai28twrgH-J82P0iF7r_Sag")
