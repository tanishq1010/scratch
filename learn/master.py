from goal_exam_extractor import goal_exam_grade_extractor
from home_data_extractor import home_data
import pandas as pd

from login_sign_up import *

from miscellaneous import *
from hero_banner_repetition_check import main
# from home_data_continue_learning import home_data



def for_all_exam_goal(goal_exam_grade):
    for ind in goal_exam_grade.index:
        print(goal_exam_grade["Goal"][ind], goal_exam_grade["Exam_name"][ind])
        signup_data=Signup()
        login_data=login(signup_data[0],"embibe1234")
        # child_data=add_user(signup_data[1],login_data[0])
        embibe_token=login_data[1]
        child_id=signup_data[1]
        home_data(child_id, goal_exam_grade["Goal"][ind], goal_exam_grade["Grade"][ind],
                  goal_exam_grade["Exam_name"][ind],
                  goal_exam_grade["Goal"][ind],embibe_token)
        # break


if __name__ == '__main__':

    df_negative_results_all_subjects = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                             'Duration', 'Type', 'Id', "Title", 'Section_name',
                                                             'Embium_counts', "Subject", "Subject_tagged",
                                                             "present in subject", "Correctly present in CG","Embibe Explainers Present","Book Section Present","Learn Section Present","Enrich Learning Present"])
    df_positive_results_all_subjects = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                             'Duration', 'Type', 'Id', "Title", 'Section_name',
                                                             'Embium_counts', "Subject", "Subject_tagged",
                                                             "present in subject", "Correctly present in CG","Embibe Explainers Present","Book Section Present","Learn Section Present","Enrich Learning Present"])
    df_negative_results_all_subjects.to_csv("negative_learn_results_all_subjects.csv", index=False)
    df_positive_results_all_subjects.to_csv("positive_learn_results_all_subjects.csv", index=False)
    df_negative_results = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                'Duration', 'Type', 'Id', "Title", 'Section_name',
                                                'Embium_counts', "Subject", "Subject_tagged", "present only once",
                                                "Correctly present in CG","Embibe Explainers Present","Book Section Present","Learn Section Present","Enrich Learning Present"])
    df_positive_results = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                'Duration', 'Type', 'Id', "Title", 'Section_name',
                                                'Embium_counts', "Subject", "Subject_tagged", "present only once",
                                                "Correctly present in CG","Embibe Explainers Present","Book Section Present","Learn Section Present","Enrich Learning Present"])
    df_negative_results.to_csv("negative_learn_results.csv", index=False)
    df_positive_results.to_csv("positive_learn_results.csv", index=False)

    # goal_exam_grade = goal_exam_grade_extractor()
    goal_exam_grade=pd.read_csv('test_file2.csv')
    for_all_exam_goal(goal_exam_grade)

    # print("\n\n COMPARING")
    comparator("positive_learn_results_all_subjects.csv", "positive_learn_results.csv")
    video_book_validation(pd.read_csv("positive_learn_results_all_subjects.csv"),"positive_learn_results_all_subjects.csv")



    # signup_data=Signup()
    # login_data=login(signup_data[0],"embibe1234")
        
    # embibe_token=login_data[1]
    # child_id=signup_data[1]
    # main(pd.read_csv('goal_exam.csv'),child_id,embibe_token)


    # df = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",'Type', 'Id', "Title", "Subject", "Subject_tagged"])
    # df.to_csv("continue_learning.csv")

    # df1=pd.read_csv("actual_continue_learning.csv")
    # home_data()
    # df2=pd.read_csv("continue_learning.csv")

    # for ind in df1.index:
    #     list1 = [""] * len(df1)
    #     df1["present in api"] = list1
    #     df_new=df2.loc[df2["Id"]==df1["Id"][ind]]
    #     if len(df_new)==1:
    #         df1["present in api"][ind]="yes"
    #     else:
    #         df1["present in api"][ind] = "no"
    #     df1.to_csv("actual_continue_learning.csv",index=False)
