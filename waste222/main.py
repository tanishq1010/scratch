import pandas as pd
from new_user_generator import signUp
import json
from API_call_method import callAPI
from update import *
import sys
import os
# from user_meta import *
import requests


def callAPI2(url, payload, method, host, token):
    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json; charset=UTF-8',
        'embibe-token': token
    }
    host = host
    response = requests.request(method, host + url, headers=headers, data=payload)

    return response


def home_data(child_id, board, grade, exam, goal, embibe_token, host):
    df = pd.read_csv('complete_video_details.csv')
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
    # print(response1.json())
    # url = f"/fiber_ms/v2/home/learn/?exam={exam}&goal={goal}&fetch_all_content=true"
    # response1 = callAPI('GET', host, url, embibe_token, '{}')

    try:

        for item in response1.json():
            if item["contentType"] == "Video":

                section = item['section_name']
                for item in item['content']:
                    try:
                        title = item['title']
                    except:
                        title = 'KEY NOT AVAILABLE'
                    try:
                        description = item['description']
                    except:
                        description = 'KEY NOT AVAILABLE'
                    try:
                        tags = item['learning_map']['tags']
                    except:
                        tags = 'KEY NOT AVAILABLE'
                    try:
                        subject_tagged = item['subject']
                    except:
                        subject_tagged = 'KEY NOT AVAILABLE'
                    try:
                        duration = item['length']
                    except:
                        duration = 'KEY NOT AVAILABLE'
                    try:
                        preview_url = item['preview_url']
                    except:
                        preview_url = "KEY NOT AVAILABLE"
                    try:
                        thumb = item['thumb']
                    except:
                        thumb = 'KEY NOT AVAILABLE'
                    try:
                        embium = item['currency']
                    except:
                        embium = 'KEY NOT AVAILABLE'
                    try:
                        topic_learnpath_name = item['learning_map']['topic_learnpath_name']
                    except:
                        topic_learnpath_name = 'KEY NOT AVAILABLE'
                    try:
                        id = item['id']
                    except:
                        id = 'KEY NOT AVAILABLE'
                    try:
                        format_id = item['learning_map']['format_id']
                    except:
                        format_id = 'KEY NOT AVAILABLE'

                    # CHECKS#_________________

                    if title == '' or title == 'KEY NOT AVAILABLE':
                        title_present = 'No'
                    else:
                        title_present = 'Yes'
                    if description == '' or description == 'KEY NOT AVAILABLE':
                        description_present = 'No'
                    else:
                        description_present = 'Yes'
                    if tags == [] or tags == 'KEY NOT AVAILABLE':
                        tags_present = 'No'
                    else:
                        tags_present = 'Yes'
                    if subject_tagged == '' or subject_tagged == 'KEY NOT AVAILABLE':
                        subject_tag_present = 'No'
                    else:
                        subject_tag_present = 'Yes'
                    if duration == '' or duration == 'KEY NOT AVAILABLE' or duration == 0:
                        duration_present = 'No'
                    else:
                        duration_present = 'Yes'
                    if thumb == '' or thumb == 'KEY NOT AVAILABLE':
                        thumb_present = 'No'
                    else:
                        thumb_present = 'Yes'
                    if embium == '' or embium == 'KEY NOT AVAILABLE':
                        embium_present = 'No'
                    else:
                        embium_present = 'Yes'

                    if preview_url == '' or preview_url == 'KEY NOT AVAILABLE':
                        preview_url_working = 'No'
                    else:
                        url = preview_url
                        if '.webm' in url or '.webp' in url:
                            response33 = callAPI2(url, '{}', 'GET', '', '')
                            try:
                                if response33.status_code == 200:
                                    preview_url_working = 'Yes'
                                else:
                                    preview_url_working = 'No'
                            except:
                                preview_url_working = response33.text
                        else:
                            preview_url_working = 'No'

                    if topic_learnpath_name == '' or topic_learnpath_name == 'KEY NOT AVAILABLE':
                        More_on_this_topic_api = 'Topic learnpath not present in api response'
                        Related_videos_api = 'topic learnpath not present in api response'
                    elif id == '' or id == 'KEY NOT AVAILABLE':
                        More_on_this_topic_api = 'id not present in api response'
                        Related_videos_api = 'id not present in api response'
                    else:
                        url11 = "/fiber_ms/v1/topics/related/" + str(topic_learnpath_name) + "?&content_id=" + str(
                            id) + "&goal=" + str(goal) + "&exam_name=" + str(exam) + "&locale=en"
                        response11 = callAPI2(url11, '{}', 'GET', host, embibe_token)
                        if response11.status_code == 200:
                            Related_videos_api = 'Yes'
                        else:
                            Related_videos_api = 'No'
                        if format_id == '' or format_id == 'KEY NOT AVAILABLE':
                            More_on_this_topic_api = 'format id is not present in api response'
                        else:
                            url22 = "/fiber_ms/topics/more/" + str(topic_learnpath_name) + "?content_id=" + str(
                                id) + "&format_id=" + str(format_id) + "&locale=en"
                            response22 = callAPI2(url22, '{}', 'GET', host, embibe_token)
                            if response22.status_code == 200:
                                More_on_this_topic_api = 'Yes'
                            else:
                                More_on_this_topic_api = 'No'
                    df.loc[len(df)] = [goal, exam, section, title_present, description_present, tags_present,
                                       subject_tag_present, duration_present, preview_url_working, embium_present,
                                       thumb_present, More_on_this_topic_api, Related_videos_api]
                    print(df)

        df.to_csv('complete_video_details.csv',index=False)
    except Exception as e:
        print(e)
        df.loc[len(df)] = [goal, exam, response1.status_code, response1.text, '', '', '',
                           '', '', '', '', '',
                           '']
        df.to_csv('complete_video_details.csv', index=False)


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


def main_function_video_learn(host, goal, exam):
    df_herobanner = pd.DataFrame(
        columns=['Goal', 'Exam', 'Section', 'Title_present', 'Decsription_present', 'Tags_present',
                 'Subject_tag_present', 'Duration_present', 'Teaser_url_working', 'Embiums_present', 'Thumb_present',
                 'More_on_this_topic_api', 'Related_videos_api'])
    df_herobanner.to_csv("complete_video_details.csv", index=False)
    goal_exam_grade = pd.read_csv('test_file2.csv')
    goal_exam_grade = goal_exam_grade[['Goal', 'Exam_name', 'Grade']]
    goal_exam_grade.drop_duplicates(inplace=True)
    goal_exam_grade.reset_index(inplace=True)
    if exam == 'All Exams':
        for_all_exam_goal(goal_exam_grade, host)
    else:
        for_particular_exam(exam, goal, host)


main_function_video_learn('https://preprodms.embibe.com', 'CBSE', '1st CBSE')
