from API_call_method import callAPI
# from utilities.test_feedback import
import pandas as pd
import json
import random
import os
from update import get_sheet_to_df


def rows_adder(df_question_wise_results):
    df_question_wise_results.insert(6, 'attempt_type', '')
    df_question_wise_results.insert(7, "Question_Displaying_in_DE", '')
    df_question_wise_results.insert(8, "Session_id", '')
    df_question_wise_results.insert(9, "Chapter_code", '')
    df_question_wise_results.insert(10, "Type", '')
    df_question_wise_results.insert(11, "Attempt_type", '')
    df_question_wise_results.insert(12, "Learnpath_name", '')
    df_question_wise_results.insert(13, "Question_id", '')


def question_qetail_extractor(df, de_response, var, Goal, Exam, user_id):
    for item in de_response.json()[var]:
        chapter_code = item['chapter_code']
        for item in item['questions']:
            attempt_type = item['attempt_type']
            learnpath_name = item['learnpath_name']
            question_code = item['question_code']
            question_id = item['question_id']
            session_id = item['session_id']
            type = item['type']
            df.loc[len(df)] = [Goal, Exam, user_id, chapter_code, question_code, question_id, attempt_type,
                               session_id, type, learnpath_name, ]


def else_function(df, var, Goal, Exam, user_id):
    df.loc[len(df)] = [Goal, Exam, user_id, '', '', '', var, '', '', '']


def De_api(host, bundle_code, student_category):
    if bundle_code == "":
        bundle_code = 'put something here'

    print('DE API WORKING RIGHT NOW')
    dictionary = {'overtime-incorrect': 'MY OVERTIME INCORRECT ATTEMPTS',
                  'overtime-correct': 'MY OVERTIME CORRECT ATTEMPTS', 'wasted-attempt': 'MY WASTED ATTEMPTS',
                  'normal-incorrect': 'QUESTIONS I GOT WRONG'}

    df = pd.DataFrame(
        columns=['Goal', 'Exam', 'User_id', 'Chapter_code', 'Question_code', 'Question_id', 'Attempt_type',
                 'Session_id', 'Type', 'Learnpath_name'])

    # test feedback running
    # test feedback running
    # test feedback running

    overtime_correct_attempts = 'overtime_correct_attempts'
    overtime_incorrect_attempts = 'overtime_incorrect_attempts'
    questions_got_wrong = 'questions_got_wrong'
    wasted_attempts = 'wasted_attempts'

    de_url = '/de/jf_analyse/revision-list-question'

    df_test_results = pd.read_csv('test_results.csv')
    df_question_wise_results = pd.read_csv('question_wise_results.csv')
    user_id = df_test_results['userId'][0]
    embibe_token = df_test_results['embibe-token'][0]
    Goal = df_test_results['Goal'][0]
    Exam = df_test_results['Exam'][0]
    learnpath_name = str(df_test_results['Goal'][0]) + '--' + str(df_test_results['Exam'][0])
    practice_taking(host, embibe_token, Goal, Exam)

    df_question_wise_results = df_question_wise_results[
        ['Goal', 'Exam', 'test_Id', 'question_code', 'Question_status_in_cg', 'fiber attemptTypeBadge']]

    df_question_wise_results_overtime_incorrect = df_question_wise_results[
        df_question_wise_results['fiber attemptTypeBadge'].str.contains('OvertimeIncorrect')]
    df_question_wise_results_wasted = df_question_wise_results[
        df_question_wise_results['fiber attemptTypeBadge'].str.contains('Wasted')]
    df_question_wise_results_overtime_correct = df_question_wise_results[
        df_question_wise_results['fiber attemptTypeBadge'].str.contains('OvertimeCorrect')]
    df_question_wise_results_incorrect = df_question_wise_results.loc[
        df_question_wise_results['fiber attemptTypeBadge'] == ('Incorrect')]
    df_question_wise_results = pd.concat([df_question_wise_results_overtime_incorrect, df_question_wise_results_wasted,
                                          df_question_wise_results_overtime_correct,
                                          df_question_wise_results_incorrect])

    payload_de_api = {
        "user_id": int(user_id),
        "learnpath_name": learnpath_name,
        "learnpath_format": "goal--exam",
        "group_by": "chapter",
        "offset": 0,
        "limit": 10000
    }

    de_response = callAPI('POST', host, de_url, embibe_token, json.dumps(payload_de_api))
    # print(de_response.json())

    if de_response.status_code == 200:
        if de_response.json()[overtime_correct_attempts]:
            question_qetail_extractor(df, de_response, overtime_correct_attempts, Goal, Exam, user_id)

        else:
            else_function(df, overtime_correct_attempts, Goal, Exam, user_id)

        if de_response.json()[overtime_incorrect_attempts]:
            question_qetail_extractor(df, de_response, overtime_incorrect_attempts, Goal, Exam, user_id)
        else:
            else_function(df, overtime_incorrect_attempts, Goal, Exam, user_id)

        if de_response.json()[questions_got_wrong]:
            question_qetail_extractor(df, de_response, questions_got_wrong, Goal, Exam, user_id)

        else:
            else_function(df, questions_got_wrong, Goal, Exam, user_id)

        if de_response.json()[wasted_attempts]:
            question_qetail_extractor(df, de_response, wasted_attempts, Goal, Exam, user_id)
        else:
            else_function(df, wasted_attempts, Goal, Exam, user_id)
        rows_adder(df_question_wise_results)

        for ind in df_question_wise_results.index:
            df_new = df.loc[df['Question_code'] == df_question_wise_results['question_code'][ind]]
            df_new.reset_index(inplace=True)

            if len(df_new) > 0:
                df_question_wise_results['Question_Displaying_in_DE'][ind] = 'Yes'
                df_question_wise_results['Session_id'][ind] = df_new['Session_id'][0]
                df_question_wise_results['Chapter_code'][ind] = df_new['Chapter_code'][0]
                df_question_wise_results['Type'][ind] = df_new['Type'][0]
                df_question_wise_results['attempt_type'][ind] = df_new['Attempt_type'][0]
                df_question_wise_results['Attempt_type'][ind] = dictionary[df_new['Attempt_type'][0]]
                df_question_wise_results['Learnpath_name'][ind] = df_new['Learnpath_name'][0]
                df_question_wise_results['Question_id'][ind] = df_new['Question_id'][0]

            else:
                df_question_wise_results['Question_Displaying_in_DE'][ind] = 'No'
                df_question_wise_results['Session_id'][ind] = 'NAN'
                df_question_wise_results['Chapter_code'][ind] = 'NAN'
                df_question_wise_results['Type'][ind] = 'NAN'
                df_question_wise_results['Attempt_type'][ind] = 'NAN'
                df_question_wise_results['Learnpath_name'][ind] = 'NAN'
                df_question_wise_results['Question_id'][ind] = "NAN"
    # except Exception as e:
    else:
        print('DE API NOT WORKING STATUS CODE IS=' + str(de_response.status_code))
        rows_adder(df_question_wise_results)

        for ind in df_question_wise_results.index:
            df_question_wise_results['Question_Displaying_in_DE'][ind] = 'DE API GAVE STATUS CODE OF ' + str(
                de_response.status_code)
            df_question_wise_results['Session_id'][ind] = 'DE API GAVE STATUS CODE OF ' + str(de_response.status_code)
            df_question_wise_results['Chapter_code'][ind] = 'DE API GAVE STATUS CODE OF ' + str(de_response.status_code)
            df_question_wise_results['Type'][ind] = 'DE API GAVE STATUS CODE OF ' + str(de_response.status_code)
            df_question_wise_results['Attempt_type'][ind] = 'DE API GAVE STATUS CODE OF ' + str(de_response.status_code)
            df_question_wise_results['Learnpath_name'][ind] = 'DE API GAVE STATUS CODE OF ' + str(
                de_response.status_code)
            df_question_wise_results['Question_id'][ind] = 'DE API GAVE STATUS CODE OF ' + str(de_response.status_code)

    df_question_wise_results.to_csv('De_api_results_for_questions_attempted.csv', index=False)

    ##Practice taking flow
    ##Practice taking flow
    ##Practice taking flow


def practice_taking(host, embibe_token, goal, exam):
    df_for_practice_data = get_sheet_to_df('1a7LGW4bPdgod3R1jC7i3jRsMOubjUCkPmHDhWatdPgY',
                                           'chapter_topics_in_sequence_chapter_level_report')
    df_for_practice_data.dropna(how='all', inplace=True)
    df_for_practice_data.fillna('NANA')

    df_for_practice_data = df_for_practice_data[
        df_for_practice_data['Chapter Present in Fiber API Response'].str.contains('Yes')]

    df_for_practice_data = df_for_practice_data[['Goal', 'Exam', 'Chapter', 'Chapter_code', 'Chapter learnpath_name']]

    df_for_practice_data = df_for_practice_data[df_for_practice_data['Goal'] == goal]
    df_for_practice_data = df_for_practice_data[df_for_practice_data['Exam'] == exam]

    df_for_practice_data = df_for_practice_data.sample()
    df_for_practice_data.reset_index(inplace=True)

    test_data = pd.read_csv('test_file2.csv')
    test_data = test_data.loc[test_data['Exam_name'] == exam]
    test_data = test_data.loc[test_data['Goal'] == goal]
    test_data.reset_index(inplace=True)

    format_refrence = test_data['Format_refrence'][0]
    lm_name = str(format_refrence) + "--" + str(df_for_practice_data['Chapter learnpath_name'][0])

    payload_practice = {
        "type": "Normal",
        "learning_map": {
            "bundle_code": df_for_practice_data['Chapter_code'][0],
            "exam_code": "kve97915",
            "level": "chapter",
            "chapter_code": df_for_practice_data['Chapter_code'][0],
            "format_id": str(format_refrence),
            "lm_name": lm_name,
            "goal_name": df_for_practice_data['Goal'][0],
            "exam_name": df_for_practice_data['Exam'][0]
        },
        "language": "en",
        "namespace": "embibe"
    }

    print(lm_name)
    embibe_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJjb3VudHJ5IjoxLCJ1c2VyX3R5cGUiOjEsInBhcmVudF91c2VyX2lkIjoxNTAwMDAzNzQ3LCJjcmVhdGVkIjoxNjExODIyOTM2LCJvcmdhbml6YXRpb25faWQiOiIxIiwiaWQiOjE1MDAwMDM5MDksImV4cCI6MTYxMzAzMjUzNiwiZGV2aWNlSWQiOiIxNjExODE5MDc4NjY0IiwibW9iaWxlX3ZlcmlmaWNhdGlvbl9zdGF0dXMiOmZhbHNlLCJlbWFpbF92ZXJpZmljYXRpb25fc3RhdHVzIjpmYWxzZSwiZW1haWwiOiIxNTAwMDAzNzQ3XzEzMjA2NDg4NjU0NzU4MTA0QGVtYmliZS11c2VyLmNvbSJ9.6kuMcIA_xf5uvSf5smOK_BOpIK5ZmMgOPamsLEwylMFJ6J5lMpWDmZ0lh6Mmg5sy1cNpyYJr8Da52PPThOttPg'
    practice_url = '/fiber_practice_ms/v1/practice/session'
    host = 'https://preprodms.embibe.com'
    pratice_session_api_response = callAPI('POST', host, practice_url, embibe_token, json.dumps(payload_practice))
    session_id = pratice_session_api_response.json()['session_id']
    os.system('git clone -b Tanishq https://tanishqr@bitbucket.org/microservicesembibe/jiofiberapiautomation.git')
    os.system(
        'cd jiofiberapiautomation/ && mvn clean test -Denv="preprod" -Dusername="abc123@auto.com" -Dpassword="test123" -DsessionID="' + session_id + '" -Dtoken="' + embibe_token + '"')

    summary_url = f"/fiber_practice_ms/v1/practice/{session_id}/summary"
    summary_api_response = callAPI('GET', host, summary_url, embibe_token, "{}")

    # for item in summary_api_response.json()['metaData']['attempts']:
    #     question_code=item['questionCode']
    #     attempttypebadge=item['attemptTypeBadge']
    #     print(question_code,attempttypebadge)

    var = (summary_api_response.json())
    print(json.dumps(var))
    os.system('rm -r jiofiberapiautomation/')


practice_taking('', '', 'CBSE', '10th CBSE')
