import pandas as pd
from new_user_generator import signUp
import json
from API_call_method import callAPI
from update import *
import sys
import os
# from user_meta import *
import requests


def callAPI2(url, payload, method, host):
    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json; charset=UTF-8',
    }
    host = host
    response = requests.request(method, host + url, headers=headers, data=payload)

    return response


def subject_data(child_id, board, grade, exam, goal, embibe_token, subject, df, host):
    payload = {
        "board": goal,
        "child_id": child_id,
        "exam": exam,
        "exam_name": exam,
        "goal": goal,
        "grade": grade,
        "onlyPractise": False,
        "fetch_all_content": True
    }

    response1 = callAPI('POST', host, f"/fiber_ms/v1/home/{subject}", embibe_token, json.dumps(payload))

    # url = f"/fiber_ms/v2/home/learn/{subject}?exam={exam}&goal={goal}&fetch_all_content=true"
    # response1 = callAPI('GET', host, url, embibe_token, '{}')

    try:
        for item in response1.json():
            if item["contentType"] == "Book":
                section = item['section_name']
                for item in item['content']:
                    try:
                        teaser_url = item['teaser_url']
                    except:
                        teaser_url = "KEY NOT AVAILABLE"
                    try:
                        title = item['title']
                    except:
                        title = 'KEY NOT FOUND'
                    if teaser_url == '' or teaser_url == 'KEY NOT AVAILABLE':
                        teaser_url_working = 'teaser url not present'
                    else:
                        url = teaser_url
                        response33 = callAPI2(url, '{}', 'GET', '')
                        try:
                            if response33.status_code == 200:
                                teaser_url_working = 'Yes'
                            else:
                                teaser_url_working = 'No'
                        except:
                            teaser_url_working = response33.text

                    df.loc[len(df)] = [f'Learn/home{subject}', goal, exam, title, section, teaser_url,
                                       teaser_url_working]
        for item in response1.json():
            if item["contentType"] == "Video":
                section = item['section_name']
                for item in item['content']:
                    try:
                        preview_url = item['preview_url']
                    except:
                        preview_url = "KEY NOT AVAILABLE"
                    try:
                        title = item['title']
                    except:
                        title = 'KEY NOT FOUND'
                    if preview_url == '' or preview_url == 'KEY NOT AVAILABLE':
                        preview_url_working = 'preview url not present'
                    else:
                        url = preview_url
                        response33 = callAPI2(url, '{}', 'GET', '')
                        try:
                            if response33.status_code == 200:
                                preview_url_working = 'Yes'
                            else:
                                preview_url_working = 'No'
                        except:
                            preview_url_working = response33.text

                    df.loc[len(df)] = [f'Learn/home{subject}', goal, exam, title, section, preview_url,
                                       preview_url_working]

    except Exception as e:
        print(e)
        df.loc[len(df)] = [f'Learn/home/{subject}', goal, exam, '', '', '', '']

    df.to_csv('teaser_urls_working_learn.csv', index=False)


def home_data(child_id, board, grade, exam, goal, embibe_token, host):
    df = pd.read_csv('teaser_urls_working_learn.csv')
    payload = {
        "board": goal,
        "child_id": child_id,
        "exam": exam,
        "exam_name": exam,
        "goal": goal,
        "grade": grade,
        "fetch_all_content": True

    }
    response1 = callAPI('POST', host, '/fiber_ms/v1/home', embibe_token,
                        json.dumps(payload))
    # url = f"/fiber_ms/v2/home/learn/?exam={exam}&goal={goal}&fetch_all_content=true"
    # response1 = callAPI('GET', host, url, embibe_token, '{}')

    try:

        for item in response1.json():
            if item["contentType"] == "Book":
                section = item['section_name']
                for item in item['content']:
                    try:
                        teaser_url = item['teaser_url']
                    except:
                        teaser_url = "KEY NOT AVAILABLE"
                    try:
                        title = item['title']
                    except:
                        title = 'KEY NOT FOUND'
                    if teaser_url == '' or teaser_url == 'KEY NOT AVAILABLE':
                        teaser_url_working = 'teaser url not present'
                    else:
                        url = teaser_url
                        response33 = callAPI2(url, '{}', 'GET', '')
                        try:
                            if response33.status_code == 200:
                                teaser_url_working = 'Yes'
                            else:
                                teaser_url_working = 'No'
                        except:
                            teaser_url_working = response33.text

                    df.loc[len(df)] = ['Learn/home', goal, exam, title, section, teaser_url, teaser_url_working]
        for item in response1.json():
            if item["contentType"] == "Video":
                section = item['section_name']
                for item in item['content']:
                    try:
                        preview_url = item['preview_url']
                    except:
                        preview_url = "KEY NOT AVAILABLE"
                    try:
                        title = item['title']
                    except:
                        title = 'KEY NOT FOUND'

                    if preview_url == '' or preview_url == 'KEY NOT AVAILABLE':
                        preview_url_working = 'preview url not present'
                    else:
                        url = preview_url
                        response33 = callAPI2(url, '{}', 'GET', '')
                        try:
                            if response33.status_code == 200:
                                preview_url_working = 'Yes'
                            else:
                                preview_url_working = 'No'
                        except:
                            preview_url_working = response33.text

                    df.loc[len(df)] = ['Learn/home', goal, exam, title, section, preview_url, preview_url_working]

        try:
            for item in response1.json():
                if item["content_section_type"] == "SUBJECTS":
                    for data in item["content"]:
                        if data["subject"] == "All Subjects":
                            continue
                        else:
                            try:
                                subject_data(child_id, board, grade, exam, goal, embibe_token, data["subject"], df,
                                             host)
                            except Exception as e:
                                print(e)

        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
        df.loc[len(df)] = ['Learn/home', goal, exam, '', response1.text, '', '']
        df.to_csv('teaser_urls_working_learn.csv', index=False)


def for_all_exam_goal(goal_exam_grade, host):
    dictionary = signUp(host)
    embibe_token = dictionary['embibe-token']
    child_id = dictionary['user_id']

    i = 0
    for ind in goal_exam_grade.index:
        print(goal_exam_grade["Goal"][ind], goal_exam_grade["Exam_name"][ind])

        home_data(child_id, goal_exam_grade["Goal"][ind], goal_exam_grade["Grade"][ind],
                  goal_exam_grade["Exam_name"][ind],
                  goal_exam_grade["Goal"][ind], embibe_token, host)


def for_particular_exam(exam, goal, host):
    dictionary = signUp(host)
    embibe_token = dictionary['embibe-token']
    child_id = dictionary['user_id']
    print(goal, exam)
    home_data(child_id, goal, '',
              exam,
              goal, embibe_token, host)


if __name__ == '__main__':

    # host = sys.argv[1]
    # goal = sys.argv[2]
    # exam = sys.argv[3]
    host = 'https://fiberdemoms.embibe.com'
    goal = 'CBSE'
    exam = '7th CBSE'

    if host == 'https://preprodms.embibe.com':
        ID = '1_5AIDjLUYNDnx7sMYMNA8CP0sCg68i3UxKCHAiv0gUo'
    else:
        ID = '1mFdO3rPW-TggUhzL_ObhGBn-gjoTgVKt9rRhCU42-qA'
    df_herobanner = pd.DataFrame(
        columns=['Screen', 'Goal', 'Exam', 'Title', 'Section', 'Teaser_url', 'Teaser_url_working'])
    df_herobanner.to_csv("teaser_urls_working_learn.csv", index=False)
    goal_exam_grade = pd.read_csv('test_file2.csv')
    goal_exam_grade = goal_exam_grade[['Goal', 'Exam_name', 'Grade']]
    goal_exam_grade.drop_duplicates(inplace=True)
    goal_exam_grade.reset_index(inplace=True)
    if exam == 'All Exams':
        for_all_exam_goal(goal_exam_grade, host)
    else:
        for_particular_exam(exam, goal, host)
