import os
import csv
import json
import string
import random
import requests
import sys
import traceback
import multiprocessing
import pandas as pd
import ast


class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Authorization': '048f38be-1b07-4b21-8f24-eac727dce217:gSEkC3dqDcIv1bbOk78UD9owjn7ins8D',
            'Content-Type': 'application/json',
        }

    def callAPI2(self, url, payload, method):
        response = requests.request(method, url, headers=self.headers, data=payload)
        # if response.status_code != 200:
        #     print(url + ' - ' + str(response.content))
        # return None
        return response

    def get_chapters(self, home_data, url):

        if url[len(url) - 1] != '/':
            url += '/'

        response1 = self.callAPI2(url, "{}", 'GET')

        if 'Exam' in response1.json():
            # goal_exams = []

            # #functions
            # with open('goal_exam.csv', 'r') as csvfile:
            #         goal_exams = list (csv.reader(csvfile, delimiter=','))

            # exams = []
            # for goal_exam in goal_exams:
            #     exams.append(goal_exam[1])

            for exam in response1.json()['Exam']:
                # print("\n\tExam: ",exam['name'])
                home_data['exam'] = exam['name']

                # if home_data['exam'] not in exams:
                #     continue
                # else:
                print("\t", home_data['exam'])

                try:
                    self.get_chapters(home_data, url + exam['name'] + "/")
                except Exception as e:
                    raise e

                # break

        elif 'Subject' in response1.json():
            for subject in response1.json()['Subject']:
                print("\t\tSubject: ", subject['name'])
                home_data['subject'] = subject['name']

                try:
                    self.get_chapters(home_data, url + subject['name'] + "/")
                except Exception as e:
                    raise e

                # break


        elif 'Unit' in response1.json():
            for unit in response1.json()['Unit']:
                print("\t\t\tUnit: ", unit['name'])
                home_data['unit'] = unit['name']

                try:
                    self.get_chapters(home_data, url + unit['name'] + "/")
                except Exception as e:
                    raise e

                # break

        elif 'Chapter' in response1.json() or 'chapter' in response1.json():
            df = pd.read_csv("Chapter_Questions.csv")
            for key in response1.json():
                for chapter in response1.json()[key]:
                    print("\t\t\t\tChapter: ", chapter['name'])
                    home_data['chapter_name'] = chapter['name']
                    chapter_id = chapter['_id']
                    print("\t\t\t\tChapter Id: ", chapter_id)
                    home_data['chapter_id'] = chapter_id

                    print("\t\t\t\t\t Getting all questions of Chapter: ", chapter['name'])
                    self.headers[
                        'Authorization'] = '048f38be-1b07-4b21-8f24-eac727dce217:gSEkC3dqDcIv1bbOk78UD9owjn7ins8D'
                    response2 = self.callAPI2('http://10.141.11.37:5000/kv_entity/' + str(
                        chapter_id) + '?embedded={%22content.practice_id%22:1}',
                                              '{}', 'GET')

                    print("\t\t\t\t\tStatus code: ", response2.status_code)
                    if response2.status_code != 200:
                        print("\t\t\t\t\tResponse: ", response2.text)
                    else:
                        try:
                            if 'practice_id' in response2.json()['content']:
                                for practice in response2.json()['content']['practice_id']:
                                    for question in practice['question_list']:
                                        df.loc[len(df)] = [home_data['goal'], home_data['Book_ID'], home_data['exam'],
                                                           home_data['subject'], home_data['unit'],
                                                           home_data['chapter_name'], home_data['chapter_id'],
                                                           int(question['question_id'])]
                                        df.to_csv("Chapter_Questions.csv", index=False)
                        except Exception as e:
                            print(traceback.format_exc())
                            df.loc[len(df)] = [home_data['goal'], home_data['Book_ID'], home_data['exam'],
                                               home_data['subject'], home_data['unit'],
                                               home_data['chapter_name'], home_data['chapter_id'],
                                               ""]
                            df.to_csv("Chapter_Questions.csv", index=False)

                # break


if __name__ == '__main__':
    # tt = {'learning_map': {'lpcode': 'kve97670--kve97915--kve98045--kve98501--kve98524--kve98525', 'subject': '', 'subject_code': '', 'exam_code': '', 'unit': '', 'chapter': '', 'author': '', 'grade': '', 'board': '', 'concept_id': '', 'format_id': '5ec5867a0c88fe5860961943', 'lm_name': 'Chemical Changes and Equations', 'topic_learnpath_name': '', 'learnpath_name': 'cbse--10th cbse--science--chemistry--chemical reactions and equations--chemical changes and equations', 'learnpath_format_name': '', 'lm_code': '', 'lm_seq': 2147483647, 'tags': [], 'mode': 'Normal'}, 'title': 'Chemical Changes and Equations', 'id': '5ec58c1f0c88fe5860972d8c', 'type': 'topic', 'content_id': '5ec5867a0c88fe5860961943/CBSE/10th CBSE/Science/Chemistry/Chemical reactions and Equations', 'thumb': 'https://content-grail-production.s3.amazonaws.com/practice-temp-tiles/1_7368GDnTYNzmGJAqATDzh1F7FSgJ5cY.webp', 'practice_tile_image': '', 'bg_thumb': '', 'subject': 'Science', 'category_url': 'https://imagin8ors-temp-dump.s3-ap-southeast-1.amazonaws.com/subject/cardicons/pun-icon.png', 'concept_count': 21, 'description': 'This topic explains the various chemical changes the carbon compounds goes under. We will also learn about the chemical equations in detail. ', 'learnmap_id': '5ec5867a0c88fe5860961943/CBSE/10th CBSE/Science/Chemistry/Chemical reactions and Equations/Chemical Changes and Equations', 'watched_duration': 0, 'practice_ids': [], 'question_book_tag': '556 Questions from 31 books', 'lpcode': 'kve97670--kve97915--kve98045--kve98501--kve98524--kve98525', 'learnpath_name': 'cbse--10th cbse--science--chemistry--chemical reactions and equations--chemical changes and equations', 'learnpath_format_name': 'goal--exam--subject--unit--chapter--topic', 'practice_progress': None}
    # print(tt['lpcode'])

    # print("\nReading goal_exam.csv")
    src = Source()

    # goals = {'Engineering':'5f17102be61885046e5d9780'}
    df = pd.DataFrame(columns=['Goal', 'Book_ID', 'Exam', 'Subject', 'Unit', 'Chapter', 'Chapter Id', 'Question Id'])
    df.to_csv("Chapter_Questions.csv", index=False)
    # df = pd.read_csv("Book_data.csv")
    # print(df)
    # df =  df.drop_duplicates(subset='book_id', keep="first")
    # print(df)
    # df.to_csv("Book_data.csv",index=False)
    df=pd.read_csv("Book_data.csv")
    # print(df)
    for ind in df.index:
        try:
            home_data = {'goal': "",
                         'Book_ID': df["book_id"][ind],
                         "exam": "", "subject": "", "unit": "", "chapter_name": "", "chapter_id": ""}
            var = "https://content-demo.embibe.com/fiber_app/learning_maps/filters/" + str(df["book_id"][ind])
            print(var)
            src.get_chapters(home_data, var)
        except Exception as e:

            print(e)
            home_data = {'goal': "",
                         'Book_ID': df["book_id"][ind],
                         "exam": "", "subject": "", "unit": "", "chapter_name": "", "chapter_id": ""}
            df1 = pd.read_csv("Chapter_Questions.csv")
            var = "https://content-demo.embibe.com/fiber_app/learning_maps/filters/" + str(df["book_id"][ind])
            print(var, '\n')
            print("\t\t\t\t\t\tSOMETHING WENT WRONG FOR ABOVE URL")
            print("------------------------------------------------------------------------------------")
            print("------------------------------------------------------------------------------------")
            print("------------------------------------------------------------------------------------")
            print("------------------------------------------------------------------------------------")
            print("------------------------------------------------------------------------------------")
            df1.loc[len(df1)] = [home_data['goal'], home_data['Book_ID'], home_data['exam'],
                                 home_data['subject'], home_data['unit'],
                                 home_data['chapter_name'], home_data['chapter_id'],
                                 "error"]
            df1.to_csv("Chapter_Questions.csv", index=False)

    # df = pd.read_csv("Question_bank.csv").drop_duplicates()
    # df1 = pd.read_csv("Chapter_Questions.csv").drop_duplicates()
    # df2 = pd.read_csv("Chapter_hygiene.csv").drop_duplicates()
    # list1 = [""] * len(df1)
    # df1["Present in CG"] = list1
    # for ind in df1.index:
    #     df_new = df.loc[df["id"] == df1["Question Id"][ind]]
    #     if len(df_new) > 0:
    #         df1["Present in CG"][ind] = "yes"
    #     else:
    #         df1["Present in CG"][ind] = "no"
    # df1.to_csv("Chapter_Questions.csv", index=False)
    #
    # list1 = [""] * len(df2)
    # df2["Questions Live"] = list1
    # for ind in df2.index:
    #     flag = 0
    #     df_new = df1.loc[df1["Exam"] == df2["Exam"][ind]]
    #     if len(df_new) > 0:
    #         df_new1 = df1.loc[df1["Goal"] == df2["Goal"][ind]]
    #         if len(df_new1) > 0:
    #             df_new2 = df1.loc[df1["Chapter"] == df2["Chapter Name"][ind]]
    #             if len(df_new2) > 0:
    #                 for ink in df_new2.index:
    #                     if df_new2["Present in CG"][ink] == "no":
    #                         flag = 1
    #                         break
    #                     else:
    #                         continue
    #                 if flag == 1:
    #                     df2["Questions Live"][ind] = "no"
    #                 else:
    #                     df2["Questions Live"][ind] = "yes"
    #             else:
    #                 df2["Questions Live"][ind] = "Not found"
    #         else:
    #             df2["Questions Live"][ind] = "Not found"
    #     else:
    #         df2["Questions Live"][ind] = "Not found"
    # df2.to_csv("Chapter_hygiene.csv", index=False)
