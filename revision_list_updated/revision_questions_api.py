from API_call_method import callAPI
# from utilities.test_feedback import
from De_api_response import De_api
import pandas as pd
import json
import random


def revision_question(host, bundle_code, student_category):
    De_api(host, bundle_code, student_category)
    print('REVISION QUESTIONS API WORKING RIGHT NOW')
    df = pd.DataFrame(
        columns=['Goal', 'Exam', 'User_id', 'Chapter_code', 'Attempt_type', 'Section_code'])

    df_test_results = pd.read_csv('test_results.csv')
    user_id = df_test_results['userId'][0]
    embibe_token = df_test_results['embibe-token'][0]
    Goal = df_test_results['Goal'][0]
    Exam = df_test_results['Exam'][0]
    df_de_results = pd.read_csv('De_api_results_for_questions_attempted.csv')

    url = "/userhome/v1/revisions/questions?learnPathFormat=Goal--Exam&learnPathName=" + Goal + "--" + Exam
    revision_question_response = callAPI("GET", host, url, embibe_token, '{}')
    if revision_question_response.status_code == 200:
        for item in revision_question_response.json():
            attempt_type = item['name']
            section_code = item['code']
            for item in item['chapters']:
                chapter_code = item['code']
                df.loc[len(df)] = [Goal, Exam, user_id, chapter_code, attempt_type, section_code]

        df_de_results.insert(14, "Chapter visible in revision questions api", '')
        df_de_results.insert(15, "Section_code", '')

        for ind in df_de_results.index:
            df_new = df.loc[df['Chapter_code'] == df_de_results['Chapter_code'][ind]]
            df_new = df_new.loc[df_new['Attempt_type'] == df_de_results['Attempt_type'][ind]]
            df_new.reset_index(inplace=True)

            if len(df_new) > 0:
                df_de_results['Chapter visible in revision questions api'][ind] = 'Yes'
                df_de_results['Section_code'][ind] = df_new['Section_code'][0]
            else:
                df_de_results['Chapter visible in revision questions api'][ind] = 'No'
                df_de_results['Section_code'][ind] = 'NAN'
    else:
        print('REVISION QUESTION API GAVE STATUS CODE=' + str(revision_question_response.status_code))
        df_de_results.insert(14, "Chapter visible in revision questions api", '')
        df_de_results.insert(15, "Section_code", '')
        for ind in df_de_results.index:
            df_de_results['Chapter visible in revision questions api'][
                ind] = 'REVISION QUESTION API GAVE STATUS CODE OF ' + str(revision_question_response.status_code)
            df_de_results['Section_code'][ind] = 'REVISION QUESTION API GAVE STATUS CODE OF ' + str(
                revision_question_response.status_code)

    df_de_results.to_csv('De_api_results_for_questions_attempted.csv', index=False)

# revision_question()
