from API_call_method import callAPI
from De_api_response import De_api
from revision_questions_api import revision_question
import pandas as pd
import json
import traceback
import random


def revision_question_details_1_level(host, bundle_code, student_category):
    revision_question(host, bundle_code, student_category)
    print('REVISION QUESTION DETAILS 1 LEVEL API WORKING RIGHT NOW')
    df = pd.DataFrame(
        columns=['Goal', 'Exam', 'User_id', 'Chapter_code', 'Question_code', 'question_identifier', 'Attempt_type'])

    df_test_results = pd.read_csv('test_results.csv')
    user_id = df_test_results['userId'][0]
    embibe_token = df_test_results['embibe-token'][0]
    Goal = df_test_results['Goal'][0]
    Exam = df_test_results['Exam'][0]
    df_revision_questions_api_response = pd.read_csv('De_api_results_for_questions_attempted.csv')
    df_revision_questions_api_response = df_revision_questions_api_response[
        ['Chapter_code', 'Section_code', 'question_code']]
    df_revision_questions_api_response.drop_duplicates(inplace=True)

    for ind in df_revision_questions_api_response.index:
        chapter_code = df_revision_questions_api_response['Chapter_code'][ind]
        section_code = df_revision_questions_api_response['Section_code'][ind]
        if chapter_code == 'NAN':
            continue
        else:
            url = f"/userhome/v1/revisions/questionDetails?chapterCode={chapter_code}&offset=0&sectionCode={section_code}&size=1000"
            revision_question_details_response = callAPI("GET", host, url, embibe_token, '{}')
            try:
                for item in revision_question_details_response.json():
                    Question_code = item['question_code']
                    Attempt_type = item['attempt_type']
                    Question_identifier = item['question_identifier']
                    df.loc[len(df)] = [Goal, Exam, user_id, chapter_code, Question_code, Question_identifier,
                                       Attempt_type]
            except:
                print(traceback.format_exc())
                print('QUESTIONS DETAILS 1 LEVEL API GAVE STATUS CODE=' + str(
                    revision_question_details_response.status_code))
                df.loc[len(df)] = [Goal, Exam, user_id, chapter_code, revision_question_details_response.text, '', '']

    df.drop_duplicates(inplace=True)
    df.reset_index(inplace=True)

    df_de_results = pd.read_csv('De_api_results_for_questions_attempted.csv')
    df_de_results.insert(16, "Question visible in Question Details api", '')
    for ind in df_de_results.index:
        df_new = df[df['Question_code'] == df_de_results['question_code'][ind]]
        df_new.reset_index(inplace=True)
        if len(df_new) > 0:
            df_de_results['Question visible in Question Details api'][ind] = 'Yes'
        else:
            df_de_results['Question visible in Question Details api'][ind] = 'No'
    df_de_results.to_csv('De_api_results_for_questions_attempted.csv', index=False)

    df.to_csv('test.csv', index=False)
