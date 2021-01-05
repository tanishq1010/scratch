from goal_exam_extractor import goal_exam_grade_extractor
from home_data_extractor import home_data
import pandas as pd
from links import  broken_link

# from login_sign_up import *
# from embibe_explainers_home import embibe_explainers_learn
# from CG_embibe_explainers import *


# from miscellaneous import *
# from home_data_continue_learning import home_data


def for_all_exam_goal(goal_exam_grade):
    for ind in goal_exam_grade.index:
        print(goal_exam_grade["Goal"][ind], goal_exam_grade["Exam_name"][ind])
        # signup_data = Signup()
        # login_data = login(signup_data[0], "embibe1234")
        # # child_data=add_user(signup_data[1],login_data[0])
        # embibe_token = login_data[1]
        # child_id = signup_data[1]
        home_data(1500001304, goal_exam_grade["Goal"][ind], goal_exam_grade["Grade"][ind],
                  goal_exam_grade["Exam_name"][ind],
                  goal_exam_grade["Goal"][ind], 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJjb3VudHJ5IjoxLCJ1c2VyX3R5cGUiOjEsImNyZWF0ZWQiOjE2MDk4NjAzOTYsIm9yZ2FuaXphdGlvbl9pZCI6IjEiLCJpZCI6MTUwMDAwMTMwNCwiZXhwIjoxNjExMDY5OTk2LCJtb2JpbGVfdmVyaWZpY2F0aW9uX3N0YXR1cyI6ZmFsc2UsImVtYWlsX3ZlcmlmaWNhdGlvbl9zdGF0dXMiOmZhbHNlLCJlbWFpbCI6IjUwNTQ1ODVfMTA5NjgwNjkzNDA0MDE2OTBAZW1iaWJlLXVzZXIuY29tIn0.bJRRZyF4eh_N7AhbjRf4SeGvKEmjObVSoTzR7SvofNJFh-BYtWROWNxi8kZaXs2LmFw7StQsg2eMc3iX0ipb4Q')
        #break


if __name__ == '__main__':
    df_negative_results = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                'Title', 'Type', 'Format_refrence', 'Section_name', 'Subject',
                                                'Subject_tagged', 'Learnpath_name', 'Learnmap_id',"Chapter"])
    df_positive_results = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                'Title', 'Type', 'Format_refrence', 'Section_name', 'Subject',
                                                'Subject_tagged', 'Learnpath_name', 'Learnmap_id',"Chapter"])
    df_negative_results.to_csv("negative_learn_results.csv", index=False)
    df_positive_results.to_csv("positive_learn_results.csv", index=False)
    df_links = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                'Title', 'Type', 'Format_refrence', 'Section_name', 'Subject',
                                                'Subject_tagged', 'Learnpath_name', 'Learnmap_id', "Chapter","book available api","recommended learning api","topics for practice chapter api present","tests in this chapter api present","bookmark question api",'about your progress api'])
    df_links.to_csv("broken links.csv",index=False)
    goal_exam_grade = goal_exam_grade_extractor()
    goal_exam_grade=pd.read_csv('test_file2.csv')
    # df=pd.read_csv("goal_exams.csv")
    for_all_exam_goal(goal_exam_grade)
    df=pd.read_csv("positive_learn_results.csv")

    broken_link(df)


    # df = pd.read_csv("positive_learn_results.csv")
    # embibe_explainers_learn(df)











