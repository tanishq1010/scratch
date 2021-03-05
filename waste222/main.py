from API_call_method import callAPI
from new_user_generator import *
from pymongo import MongoClient
import pandas as pd


def fiber_contries(response):
    df = pd.DataFrame(
        columns=['Goal', 'Exam_name', 'Exam_code', 'Format_refrence', 'Goal_code', 'Goal_name', 'Exam_name', 'Grade'])
    for item in response.json()['data']:
        goal = item['name']
        goal_name = item['display_name']
        goal_code = item['code']
        for item in item['exam']:
            exam = item['name']
            exam_name = item['display_name']
            exam_code = item['code']
            format_refrence = item['format_reference']
            grade = item['grade']

            df.loc[len(df)] = [goal, exam, exam_code, format_refrence, goal_code, goal_name, exam_name, grade]
    df.to_csv('testfile2.csv', index=False)


def callAPI1(url, payload, method, token):
    headers = {'Connection': 'keep-alive', 'Accept': '*/*', 'Content-Type': 'application/json', "embibe-token": token}
    response = requests.request(method, url, headers=headers, data=payload)

    return response


def change_end_point(end_point):
    ans = ""

    switcher = {
        '?': '%3F',
        ' ': '%20',
        '': '%21',
        '"': '%22',
        '%': '%25',
        '&': '%26',
        '/': '%2F'
    }
    for s in end_point:
        ans += switcher.get(s, s)

    return ans


def main(child_id, board, grade, exam, goal, embibe_token, host, format_refrence, exam_code, goal_code, display_exam,
         display_goal):
    df_positive_results = pd.read_csv("positive_learn_results.csv")
    payload = {
        "board": goal,
        "child_id": child_id,
        "exam": exam,
        "exam_name": exam,
        "goal": goal,
        "grade": grade,
        "fetch_all_content": True
    }
    # url=f"/fiber_ms/v2/home/learn/?exam={exam}&goal={goal}&fetch_all_content=True"
    # response1 = callAPI('GET', host, url, embibe_token, '{}')
    response1 = callAPI('POST', host, '/fiber_ms/v1/home', embibe_token,
                        json.dumps(payload))

    try:
        for item in response1.json():
            # if item["contentType"] == "learn_chapter":
            #     try:
            #         section_name = item["section_name"]
            #     except:
            #         section_name = None
            #     for data in item["content"]:
            #         try:
            #             Type = data["type"]
            #         except:
            #             Type = None
            #         try:
            #             subject_tagged = data["subject"]
            #         except:
            #             subject_tagged = None
            #         try:
            #             learnpath_name = data["learnpath_name"]
            #         except:
            #             learnpath_name = None
            #         try:
            #             learnmap_id = data['learnmap_id']
            #             learnmap_id = change_end_point(learnmap_id)
            #         except:
            #             learnmap_id = None
            #         try:
            #             Id = data['id']
            #         except:
            #             Id = None
            #         try:
            #             learnpath_format_name = data['learnpath_format_name']
            #         except:
            #             learnpath_format_name = None
            #
            #         df_positive_results.loc[len(df_positive_results)] = [exam, goal, display_exam, display_goal,
            #                                                              exam_code, goal_code, grade, Type,
            #                                                              format_refrence,
            #                                                              section_name, subject_tagged, learnpath_name,
            #                                                              learnmap_id, Id, learnpath_format_name]
            #         # df_positive_results.to_csv("positive_learn_results.csv", index=False)
            if item["contentType"] == "Video":
                try:
                    section_name = item["section_name"]
                except:
                    section_name = None
                for data in item["content"]:
                    try:
                        Type = data["type"]
                    except:
                        Type = None
                    try:
                        subject_tagged = data["subject"]
                    except:
                        subject_tagged = None
                    try:
                        learnpath_name = data['learning_map']["topic_learnpath_name"]
                    except:
                        learnpath_name = None
                    try:
                        learnmap_id = learnpath_name.replace('--', '/')
                        learnmap_id = change_end_point(learnmap_id)
                    except:
                        learnmap_id = None
                    try:
                        Id = data['id']
                    except:
                        Id = None
                    try:
                        learnpath_format_name = data['learning_map']['learnpath_format_name']
                    except:
                        learnpath_format_name = None

                    df_positive_results.loc[len(df_positive_results)] = [exam, goal, display_exam, display_goal,
                                                                         exam_code, goal_code, grade, Type,
                                                                         format_refrence,
                                                                         section_name, subject_tagged, learnpath_name,
                                                                         learnmap_id, Id, learnpath_format_name]
            # if item["contentType"] == "Book":
            #     try:
            #         section_name = item["section_name"]
            #     except:
            #         section_name = None
            #     for data in item["content"]:
            #         try:
            #             Type = data["type"]
            #         except:
            #             Type = None
            #         try:
            #             subject_tagged = data["subject"]
            #         except:
            #             subject_tagged = None
            #         try:
            #             learnpath_name = data['learning_map']["topic_learnpath_name"]
            #         except:
            #             learnpath_name = None
            #         try:
            #             learnmap_id = learnpath_name.replace('--', '/')
            #             learnmap_id = change_end_point(learnmap_id)
            #         except:
            #             learnmap_id = None
            #         try:
            #             Id = data['id']
            #         except:
            #             Id = None
            #         try:
            #             learnpath_format_name = data['learning_map']['learnpath_format_name']
            #         except:
            #             learnpath_format_name = None
            #
            #         df_positive_results.loc[len(df_positive_results)] = [exam, goal, display_exam, display_goal,
            #                                                              exam_code, goal_code, grade, Type,
            #                                                              format_refrence,
            #                                                              section_name, subject_tagged, learnpath_name,
            #                                                              learnmap_id, Id, learnpath_format_name]

        df_positive_results.to_csv("positive_learn_results.csv", index=False)

    except:
        df_positive_results.loc[len(df_positive_results)] = [exam, goal, display_exam, display_goal, exam_code,
                                                             goal_code, grade, response1.text,
                                                             format_refrence,
                                                             '', '', '',
                                                             '', '', '']
        df_positive_results.to_csv("positive_learn_results.csv", index=False)


def home_data(child_id, board, grade, exam, goal, embibe_token, host, format_refrence, exam_code, goal_code,
              display_exam, display_goal):
    main(child_id, board, grade, exam, goal, embibe_token, host, format_refrence, exam_code, goal_code, display_exam,
         display_goal)


def for_all_exam_goal(goal_exam_grade, host, embibe_token, child_id):
    for ind in goal_exam_grade.index:
        print(goal_exam_grade["Goal"][ind], goal_exam_grade["Exam_name"][ind])
        format_refrence = goal_exam_grade['Format_refrence'][ind]
        exam_code = goal_exam_grade['Exam_code'][ind]
        goal_code = goal_exam_grade['Goal_code'][ind]
        display_goal = goal_exam_grade['Goal_name'][ind]
        display_exam = goal_exam_grade['Exam_name'][ind]

        home_data(child_id, goal_exam_grade["Goal"][ind], goal_exam_grade["Grade"][ind],
                  goal_exam_grade["Exam_name"][ind],
                  goal_exam_grade["Goal"][ind],
                  embibe_token, host, format_refrence, exam_code, goal_code, display_exam, display_goal)
        # break


def extractor(exam, goal, grade, host):
    df_positive_results = pd.DataFrame(
        columns=['Exam', 'Goal', 'Display_exam', 'Display_goal', 'Exam_code', 'Goal_code', "Grade",
                 'Type', 'Format_refrence', 'Section_name',
                 'Subject_tagged', 'Learnpath_name', 'Learnmap_id', 'Id',
                 'Learnpath_format_name'])

    df_positive_results.to_csv("positive_learn_results.csv", index=False)
    response11 = callAPI1(host + '/content_ms_fiber/v1/embibe/en/fiber-countries-goals-exams',
                          "{}", 'GET', '')
    fiber_contries(response11)

    if exam == "All Exams":
        goal_exam_grade = pd.read_csv('test123.csv')
        dictionary = signUp(host)
        embibe_token = dictionary['embibe-token']
        child_id = dictionary['user_id']
        for_all_exam_goal(goal_exam_grade, host, embibe_token, child_id)
extractor('All Exams','','','https://preprodms.embibe.com')