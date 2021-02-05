import pandas as pd
from new_user_generator import signUp
import json
from API_call_method import callAPI


def minutes_converter(duration_given):
        mins = int(duration_given / 60)
        expected_duration_display = str(mins)
        if mins > 1:
            expected_duration_display += " mins"
        else:
            expected_duration_display += " min"

        sec = int(duration_given % 60)
        if sec != 0:
            if expected_duration_display != "":
                expected_duration_display += " " + str(sec) + " sec"
            else:
                expected_duration_display += str(sec) + " sec"
        return expected_duration_display




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
    flag = 0
    for item in response1.json():
        if item["content_section_type"] == "HEROBANNER":
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
                        ID = item['id']
                    except:
                        ID = 'KEY NOT AVAILABLE'
                    try:
                        learnpath = item['learning_map']['topic_learnpath_name']
                    except:
                        learnpath = 'KEY NOT AVAILABLE'
                    try:
                        LIST = str(item['learning_map']['topic_learnpath_name']).split("--")
                        tagged_exam = LIST[1]
                    except:
                        tagged_exam = 'KEY NOT AVAILABLE'
                    try:
                        teaser_url = item['teaser_url']
                    except:
                        teaser_url = 'KEY NOT AVAILABLE'
                    title1 = title
                    description1 = description
                    learnpath1 = learnpath
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
                    tagged_exam_correct = 'Na'
                    if tagged_exam != '' and tagged_exam != 'KEY NOT AVAILABLE':
                        if exam.lower() == tagged_exam.lower():
                            tagged_exam_correct = 'Yes'
                        else:
                            tagged_exam_correct = 'No'
                    else:
                        tagged_exam_correct = 'No'
                    if teaser_url != '' and teaser_url != 'KEY NOT AVAILABLE':
                        teaser_url = 'Yes'
                    else:
                        teaser_url = 'No'
                    duration_in_cg = 'Na'
                    if ID != '' and ID != 'KEY NOT AVAILABLE':
                        url = "/learning_objects?where={%22type%22:%22Video%22,%22id%22:" + str(ID) + "}"
                        response2 = callAPI('GET', 'https://content-demo.embibe.com', url,
                                            '048f38be-1b07-4b21-8f24-eac727dce217:gSEkC3dqDcIv1bbOk78UD9owjn7ins8D',
                                            '{}')
                        try:
                            for var in response2.json()['_items']:
                                duration_in_cg = var['content']['source_attributes']['duration']
                                status = var['status']
                        except:
                            duration_in_cg = 'KEY NOT AVAILABLE'
                            status = 'KEY NOT AVAILABLE'
                    expected_duration_display = 'Na'
                    if duration_in_cg != 'KEY NOT AVAILABLE':
                        expected_duration_display = minutes_converter(duration_in_cg)
                    if expected_duration_display == duration_display and duration_in_cg >= 5:
                        is_duration_okay = 'Yes'
                    else:
                        is_duration_okay = 'No'

                    if subject_tagged.lower() == subject.lower():
                        is_subject_tagged_correct = 'Yes'
                    else:
                        is_subject_tagged_correct = 'No'

                    df.loc[len(df)] = [f"Learn/home/{subject}", goal, exam, tagged_exam, tagged_exam_correct, subject,
                                       subject_tagged, is_subject_tagged_correct, ID, duration_in_cg, duration_display,
                                       expected_duration_display, is_duration_okay, embium_coins, title, description,
                                       image_url, video_url, teaser_url, status, title1, description1, learnpath1]

    # print(df)
    if flag == 0:
        df.loc[len(df)] = [f"Learn/home/{subject}", goal, exam, 'HEROBANNER NOT FOUND', '', subject,
                           '', '', '', '', '',
                           '', '', '', '', '',
                           '', '', '', '', '', '', '']

    df.to_csv('Herobanner_check.csv', index=False)


def home_data(child_id, board, grade, exam, goal, embibe_token, host):
    df = pd.read_csv('Herobanner_check.csv')
    # print(df)
    payload = {
        "board": goal,
        "child_id": child_id,
        "exam": exam,
        "exam_name": exam,
        "goal": goal,
        "grade": grade,
        "fetch_all_content": True
    }

    response1 = callAPI('POST', host, f"/fiber_ms/v1/home", embibe_token, json.dumps(payload))
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
        if item["content_section_type"] == "HEROBANNER":
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
                        ID = item['id']
                    except:
                        ID = 'KEY NOT AVAILABLE'
                    try:
                        learnpath = item['learning_map']['topic_learnpath_name']
                    except:
                        learnpath = 'KEY NOT AVAILABLE'
                    try:
                        LIST = str(item['learning_map']['topic_learnpath_name']).split("--")
                        tagged_exam = LIST[1]
                    except:
                        tagged_exam = 'KEY NOT AVAILABLE'
                    try:
                        teaser_url = item['teaser_url']
                    except:
                        teaser_url = 'KEY NOT AVAILABLE'
                    title1 = title
                    description1 = description
                    learnpath1 = learnpath
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

                    if tagged_exam != '' and tagged_exam != 'KEY NOT AVAILABLE':
                        if exam.lower() == tagged_exam.lower():
                            tagged_exam_correct = 'Yes'
                        else:
                            tagged_exam_correct = 'No'
                    else:
                        tagged_exam_correct = 'No'
                    # print(teaser_url)
                    if teaser_url != '' and teaser_url != 'KEY NOT AVAILABLE':
                        teaser_url = 'Yes'
                    else:
                        teaser_url = 'No'
                    duration_in_cg = 'Na'
                    if ID != '' and ID != 'KEY NOT AVAILABLE':
                        url = "/learning_objects?where={%22type%22:%22Video%22,%22id%22:" + str(ID) + "}"
                        response2 = callAPI('GET', 'https://content-demo.embibe.com', url,
                                            '048f38be-1b07-4b21-8f24-eac727dce217:gSEkC3dqDcIv1bbOk78UD9owjn7ins8D',
                                            '{}')
                        try:
                            for var in response2.json()['_items']:
                                duration_in_cg = var['content']['source_attributes']['duration']
                                status = var['status']
                        except:
                            duration_in_cg = 'KEY NOT AVAILABLE'
                            status = 'KEY NOT AVAILABLE'
                    expected_duration_display = 'Na'
                    if duration_in_cg != 'KEY NOT AVAILABLE':
                        expected_duration_display = minutes_converter(duration_in_cg)
                    if expected_duration_display == duration_display and duration_in_cg >= 5:
                        is_duration_okay = 'Yes'
                    else:
                        is_duration_okay = 'No'

                    if subject_tagged in LIST22:
                        is_subject_tagged_correct = 'Yes'
                    else:
                        is_subject_tagged_correct = 'No'

                    df.loc[len(df)] = ['Learn/home', goal, exam, tagged_exam, tagged_exam_correct, 'All Subjects',
                                       subject_tagged, is_subject_tagged_correct, ID, duration_in_cg, duration_display,
                                       expected_duration_display, is_duration_okay, embium_coins, title, description,
                                       image_url, video_url, teaser_url, status, title1, description1, learnpath1]
        # print(df)
    if flag == 0:
        if flag == 0:
            df.loc[len(df)] = [f"Learn/home", goal, exam, 'HEROBANNER NOT FOUND', 'All Subject', '',
                               '', '', '', '', '',
                               '', '', '', '', '',
                               '', '', '', '', '', '', '']

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

        print(goal_exam_grade["Goal"][ind], goal_exam_grade["Exam_name"][ind])

        try:
            home_data(child_id, goal_exam_grade["Goal"][ind], goal_exam_grade["Grade"][ind],
                      goal_exam_grade["Exam_name"][ind],
                      goal_exam_grade["Goal"][ind], embibe_token, host)
        except Exception as e:
            print(e)
            print(print(goal_exam_grade["Goal"][ind], goal_exam_grade["Exam_name"][ind]))
            print("ABOVE GOAL EXAM GAVE ERROR")
        # i += 1
        # if i > 6:
        #     break


if __name__ == '__main__':
    host = 'https://preprodms.embibe.com'
    df_herobanner = pd.DataFrame(
        columns=['Screen', 'Goal', 'Exam', 'Exam_tagged', 'Is_exam_tagged_correct', 'Subject', 'Subject_tagged',
                 'Is_subject_tagged_correct', 'Video_id', 'Duration_given', 'Duration_display',
                 'Expected_duration_display', 'Is_duration_okay', 'Embium_coins', 'Is_title_present',
                 'Is_description_< 150_character', 'Image_url_present', 'Video_url_present',
                 'Teaser_url_present', 'Status', 'Title', 'Description', 'Learn_path'])
    df_herobanner.to_csv("Herobanner_check.csv", index=False)
    goal_exam_grade = pd.read_csv('test_file2.csv')
    for_all_exam_goal(goal_exam_grade, host)
