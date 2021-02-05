import pandas as pd
from new_user_generator import signUp
import json
from API_call_method import callAPI
from Book_extractor import get_active_book_list


def subject_data(child_id, board, grade, exam, goal, embibe_token, subject, df, host):
    df1 = pd.read_csv('Books_List.csv')
    payload = {
        "board": goal,
        "child_id": child_id,
        "exam": exam,
        "exam_name": exam,
        "goal": goal,
        "grade": grade,
        "onlyPractise": True,
        "fetch_all_content": True
    }
    response1 = callAPI('POST', host, f"/fiber_ms/v1/home/{subject}", embibe_token, json.dumps(payload))
    flag = 0
    for item in response1.json():
        if item["content_section_type"] == "PRACTICEBANNER":
            flag = 1
            for item in item['content']:
                for item in item['data']:
                    try:
                        embium_coins = item['embium_coins']
                    except:
                        embium_coins = "KEY NOT AVAILABLE"
                    try:
                        title = item['title']
                    except:
                        title = "KEY NOT AVAILABLE"
                    try:
                        image_url = item['image_url']
                    except:
                        image_url = "KEY NOT AVAILABLE"
                    try:
                        video_url = item['video_url']
                    except:
                        video_url = "KEY NOT AVAILABLE"
                    try:
                        description = item['description']
                    except:
                        description = 'KEY NOT AVAILABLE'
                    try:
                        duration_display = item['duration']
                    except:
                        duration_display = 'KEY NOT AVAILABLE'
                    try:
                        subject_tagged = item['subject']
                    except:
                        subject_tagged = 'KEY NOT AVAILABLE'
                    try:
                        ID = item['book_id']
                    except:
                        ID = 'KEY NOT AVAILABLE'
                    try:
                        teaser_url = item['teaser_url']
                    except:
                        teaser_url = 'KEY NOT AVAILABLE'
                    title1 = title
                    description1 = description
                    if title != "" and title != 'KEY NOT AVAILABLE':
                        title = 'Yes'
                    else:
                        title = 'No'
                    if image_url != "" and image_url != 'KEY NOT AVAILABLE':
                        image_url = 'Yes'
                    else:
                        image_url = 'No'
                    if video_url != "" and video_url != 'KEY NOT AVAILABLE':
                        video_url = 'Yes'
                    else:
                        video_url = 'No'
                    if description != '' and description != 'KEY NOT AVAILABLE' and len(description) <= 150:
                        description = 'Yes'
                    else:
                        description = 'No'
                    if teaser_url != '' and teaser_url != 'KEY NOT AVAILABLE':
                        teaser_url = 'Yes'
                    else:
                        teaser_url = 'No'

                    df_new = df1.loc[(df1['Book Id']).str.contains(ID.lower())]
                    df_new = df_new.loc[df_new['Exam'] == exam]
                    if len(df_new) > 0:
                        tagged_exam = exam
                    else:
                        tagged_exam = 'Not available'

                    if tagged_exam != '' and tagged_exam != 'KEY NOT AVAILABLE':
                        if exam.lower() == tagged_exam.lower():
                            tagged_exam_correct = 'Yes'
                        else:
                            tagged_exam_correct = 'No'
                    else:
                        tagged_exam_correct = 'No'

                    if subject_tagged in subject:
                        is_subject_tagged_correct = 'Yes'
                    else:
                        is_subject_tagged_correct = 'No'
                    url = f"/fiber_ms/book?book_id={ID}&type=NormalBook"
                    response2 = callAPI('GET', 'https://preprodms.embibe.com', url, '', '{}')
                    book_toc_description = response2.json()['data']['description']

                    if book_toc_description == description:
                        Does_description_match_book_toc = 'Yes'
                    else:
                        Does_description_match_book_toc = 'No'
                    if response2.status_code == 200:
                        practice_now = 'Yes'
                    else:
                        practice_now = 'No'
                    if duration_display != '' and duration_display != 'KEY NOT AVAILABLE':
                        concept_present = 'Yes'
                    else:
                        concept_present = 'No'

                    df.loc[len(df)] = [f'Practice/home/{subject}', goal, exam, tagged_exam, tagged_exam_correct,
                                       subject,
                                       subject_tagged, is_subject_tagged_correct, ID, duration_display, concept_present,
                                       embium_coins,
                                       title, description, Does_description_match_book_toc, image_url, video_url,
                                       teaser_url, title1, description1, practice_now]

    if flag == 0:
        df.loc[len(df)] = [f'Practice/home/{subject}', goal, exam, 'PRACTICE BANNER NOT PRESENT', '', subject,
                           '', '', '', '', '', '',
                           '', '', '', '', '',
                           '', '', '', '']

    df.to_csv('practicebanner_check.csv', index=False)


def home_data(child_id, board, grade, exam, goal, embibe_token, host):
    df = pd.read_csv('practicebanner_check.csv')
    df1 = pd.read_csv('Books_List.csv')
    payload = {
        "board": goal,
        "child_id": child_id,
        "exam": exam,
        "exam_name": exam,
        "goal": goal,
        "grade": grade
    }

    response1 = callAPI('POST', host, f"/fiber_ms/v1/home/practise", embibe_token, json.dumps(payload))
    LIST22 = []
    try:
        for item in response1.json():
            if item["content_section_type"] == "SUBJECTS":
                for data in item["content"]:
                    if data["subject"] == "All Subjects":
                        continue
                    else:
                        try:
                            LIST22.append(data['subject'])
                        except Exception as e:
                            print(e)

    except Exception as e:
        print(e)
    flag = 0
    for item in response1.json():
        if item["content_section_type"] == "PRACTICEBANNER":
            flag = 1
            for item in item['content']:
                for item in item['data']:
                    try:
                        embium_coins = item['embium_coins']
                    except:
                        embium_coins = "KEY NOT AVAILABLE"
                    try:
                        title = item['title']
                    except:
                        title = "KEY NOT AVAILABLE"
                    try:
                        image_url = item['image_url']
                    except:
                        image_url = "KEY NOT AVAILABLE"
                    try:
                        video_url = item['video_url']
                    except:
                        video_url = "KEY NOT AVAILABLE"
                    try:
                        description = item['description']
                    except:
                        description = 'KEY NOT AVAILABLE'
                    try:
                        duration_display = item['duration']
                    except:
                        duration_display = 'KEY NOT AVAILABLE'
                    try:
                        subject_tagged = item['subject']
                    except:
                        subject_tagged = 'KEY NOT AVAILABLE'
                    try:
                        ID = item['book_id']
                    except:
                        ID = 'KEY NOT AVAILABLE'
                    try:
                        teaser_url = item['teaser_url']
                    except:
                        teaser_url = 'KEY NOT AVAILABLE'
                    title1 = title
                    description1 = description
                    if title != "" and title != 'KEY NOT AVAILABLE':
                        title = 'Yes'
                    else:
                        title = 'No'
                    if image_url != "" and image_url != 'KEY NOT AVAILABLE':
                        image_url = 'Yes'
                    else:
                        image_url = 'No'
                    if video_url != "" and video_url != 'KEY NOT AVAILABLE':
                        video_url = 'Yes'
                    else:
                        video_url = 'No'
                    if description != '' and description != 'KEY NOT AVAILABLE' and len(description) <= 150:
                        description = 'Yes'
                    else:
                        description = 'No'
                    if teaser_url != '' and teaser_url != 'KEY NOT AVAILABLE':
                        teaser_url = 'Yes'
                    else:
                        teaser_url = 'No'

                    df_new = df1.loc[(df1['Book Id']).str.contains(ID.lower())]
                    df_new = df_new.loc[df_new['Exam'] == exam]
                    if len(df_new) > 0:
                        tagged_exam = exam
                    else:
                        tagged_exam = 'Not available'

                    if tagged_exam != '' and tagged_exam != 'KEY NOT AVAILABLE':
                        if exam.lower() == tagged_exam.lower():
                            tagged_exam_correct = 'Yes'
                        else:
                            tagged_exam_correct = 'No'
                    else:
                        tagged_exam_correct = 'No'

                    if subject_tagged in LIST22:
                        is_subject_tagged_correct = 'Yes'
                    else:
                        is_subject_tagged_correct = 'No'
                    url = f"/fiber_ms/book?book_id={ID}&type=NormalBook"
                    response2 = callAPI('GET', 'https://preprodms.embibe.com', url, '', '{}')
                    book_toc_description = response2.json()['data']['description']

                    if book_toc_description == description:
                        Does_description_match_book_toc = 'Yes'
                    else:
                        Does_description_match_book_toc = 'No'
                    if response2.status_code == 200:
                        practice_now = 'Yes'
                    else:
                        practice_now = 'No'
                    if duration_display != '' and duration_display != 'KEY NOT AVAILABLE':
                        concept_present = 'Yes'
                    else:
                        concept_present = 'No'

                    df.loc[len(df)] = ['Practice/home', goal, exam, tagged_exam, tagged_exam_correct, 'All Subjects',
                                       subject_tagged, is_subject_tagged_correct, ID, duration_display, concept_present,
                                       embium_coins,
                                       title, description, Does_description_match_book_toc, image_url, video_url,
                                       teaser_url, title1, description1, practice_now]

    if flag == 0:
        df.loc[len(df)] = ['Practice/home', goal, exam, 'PRACTICE BANNER NOT PRESENT', '', 'All Subjects',
                           '', '', '', '', '', '',
                           '', '', '', '', '',
                           '', '', '', '']

    try:
        for item in response1.json():
            if item["content_section_type"] == "SUBJECTS":
                for data in item["content"]:
                    if data["subject"] == "All Subjects":
                        continue
                    else:
                        try:
                            subject_data(child_id, board, grade, exam, goal, embibe_token, data["subject"], df, host)
                        except Exception as e:
                            print(e)

    except Exception as e:
        print(e)


def for_all_exam_goal(goal_exam_grade, host):

    dictionary = signUp('https://preprodms.embibe.com')
    embibe_token = dictionary['embibe-token']
    child_id = dictionary['user_id']
    i = 0
    for ind in goal_exam_grade.index:
        # print(goal_exam_grade["Goal"][ind])
        if goal_exam_grade["Goal"][ind] == 'Telangana Board':

            print(goal_exam_grade["Goal"][ind], goal_exam_grade["Exam_name"][ind])

            try:
                home_data(child_id, goal_exam_grade["Goal"][ind], goal_exam_grade["Grade"][ind],
                          goal_exam_grade["Exam_name"][ind],
                          goal_exam_grade["Goal"][ind], embibe_token, host)
            except Exception as e:
                print(e)
                print(print(goal_exam_grade["Goal"][ind], goal_exam_grade["Exam_name"][ind]))
                print("ABOVE GOAL EXAM GAVE ERROR")
        else:
            continue
        # i += 1
        # if i > 2:
        #     break


if __name__ == '__main__':
    get_active_book_list()
    host = 'https://preprodms.embibe.com'
    df_practicebanner = pd.DataFrame(
        columns=['Screen', 'Goal', 'Exam', 'Exam_tagged', 'Is_exam_tagged_correct', 'Subject', 'Subject_tagged',
                 'Is_subject_tagged_correct', 'Book_id', 'Concept', 'Concept_present', 'Embium_coins',
                 'Is_title_present',
                 'Is_description_less_150_character_range', 'Does_description_match_book_toc', 'Image_url_present',
                 'Video_url_present',
                 'Teaser_url_present', 'Title', 'Description', 'Practice_now_button_taking_to_book_toc'])
    df_practicebanner.to_csv("practicebanner_check.csv", index=False)
    goal_exam_grade = pd.read_csv('test_file2.csv')
    for_all_exam_goal(goal_exam_grade, host)
