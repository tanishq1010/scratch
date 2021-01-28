from API_call_method import callAPI
from De_api_response import De_api
from revision_questions_api import revision_question
from revision_question_details_1 import revision_question_details_1_level
import pandas as pd
import json
import random


def revision_question_details_2_level(host, bundle_code, student_category):
    revision_question_details_1_level(host, bundle_code, student_category)
    print('REVISION QUESTION DETAILS 2 LEVEL API WORKING RIGHT NOW')

    df_test_results = pd.read_csv('test_results.csv')
    embibe_token = df_test_results['embibe-token'][0]

    df_de_results = pd.read_csv('De_api_results_for_questions_attempted.csv')

    df_de_results.insert(17, "Question visible in second Question Details api", '')

    for ind in df_de_results.index:
        session_id = df_de_results['Session_id'][ind]
        question_type = df_de_results['Type'][ind]
        question_code = df_de_results['question_code'][ind]
        print(question_code)
        if question_type == 'test':
            question_id = df_de_results['question_code'][ind]
        else:
            question_id = df_de_results['Question_id'][ind]
        url = f"/userhome/v1/{session_id}/question/{question_id}?questionType={question_type}"
        details_api_response = callAPI("GET", host, url, embibe_token, '{}')
        if details_api_response.status_code == 200:
            if details_api_response.json()['code'] == question_code:
                df_de_results['Question visible in second Question Details api'][ind] = "Yes"
            else:
                df_de_results['Question visible in second Question Details api'][ind] = "No"
        else:
            df_de_results['Question visible in second Question Details api'][ind] = details_api_response.text

    df_de_results.to_csv('De_api_results_for_questions_attempted.csv', index=False)


revision_question_details_2_level('https://preprodms.embibe.com', "", "Fighter")
