from goal_exam_extractor import goal_exam_grade_extractor
from home_data_extractor import home_data
import pandas as pd

from login_sign_up import *

from miscellaneous import *
from hero_banner_repetition_check import main
from home_data_extractor_video_sequence import home_data1
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
#         break


if __name__ == '__main__':

    df_negative_results_all_subjects = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                             'Duration', 'Type', 'Id', "Title", 'Section_name',
                                                             'Embium_counts', "Subject", "Subject_tagged",
                                                             "present in subject", "Correctly present in CG","Embibe Explainers Present","Book Section Present","Learn Section Present","Enrich Learning Present",'description present'])
    df_positive_results_all_subjects = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                             'Duration', 'Type', 'Id', "Title", 'Section_name',
                                                             'Embium_counts', "Subject", "Subject_tagged",
                                                             "present in subject", "Correctly present in CG","Embibe Explainers Present","Book Section Present","Learn Section Present","Enrich Learning Present",'description present'])
    df_negative_results_all_subjects.to_csv("negative_learn_results_all_subjects.csv", index=False)
    df_positive_results_all_subjects.to_csv("positive_learn_results_all_subjects.csv", index=False)
    df_negative_results = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                'Duration', 'Type', 'Id', "Title", 'Section_name',
                                                'Embium_counts', "Subject", "Subject_tagged", "present only once",
                                                "Correctly present in CG","Embibe Explainers Present","Book Section Present","Learn Section Present","Enrich Learning Present",'description present'])
    df_positive_results = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                'Duration', 'Type', 'Id', "Title", 'Section_name',
                                                'Embium_counts', "Subject", "Subject_tagged", "present only once",
                                                "Correctly present in CG","Embibe Explainers Present","Book Section Present","Learn Section Present","Enrich Learning Present",'description present'])
    df_negative_results.to_csv("negative_learn_results.csv", index=False)
    df_positive_results.to_csv("positive_learn_results.csv", index=False)

    goal_exam_grade = pd.read_csv('test_file2.csv')
    # goal_exam_grade_extractor()
    for_all_exam_goal(goal_exam_grade)

    # print("\n\n COMPARING")
    comparator("positive_learn_results_all_subjects.csv", "positive_learn_results.csv")
    comparator2("positive_learn_results_all_subjects.csv", "positive_learn_results.csv")

    video_book_validation(pd.read_csv("positive_learn_results_all_subjects.csv"),"positive_learn_results_all_subjects.csv")
    video_book_validation(pd.read_csv("positive_learn_results.csv"),"positive_learn_results.csv")

    df1=pd.read_csv('positive_learn_results_all_subjects.csv')
    df1.to_csv('positive_learn_results_all_subjects.csv', na_rep='NA',index=False)
    df2=pd.read_csv('positive_learn_results.csv')
    df2.to_csv('positive_learn_results.csv',index=False,na_rep='NA')

    # df3=pd.read_csv('negative_learn_results_all_subjects.csv')
    # df3.to_csv('negative_learn_results_all_subjects.csv',index=False,na_rep='NA')

    # df4=pd.read_csv('negative_learn_results.csv')
    # df4.to_csv('negative_learn_results.csv',index=False,na_rep='NA')


    # signup_data=Signup()
    # login_data=login(signup_data[0],"embibe1234")
        
    # embibe_token=login_data[1]
    # child_id=signup_data[1]
    # main(pd.read_csv('goal_exam.csv'),child_id,embibe_token)

    
    
    # df = pd.DataFrame(columns=['Child_id', 'Exam', 'Goal', 'Title','Id','Subject'])
       
    # df.to_csv("video_sequence.csv",index=False)
    # for ind in goal_exam_grade.index:
    #     goal=goal_exam_grade["Goal"][ind]
    #     exam=goal_exam_grade["Exam_name"][ind]

    #     grade = goal_exam_grade["Grade"][ind]
    #     board=goal
    #     home_data1(child_id, board, grade, exam, goal, embibe_token)
    
    # -------------------------------------------------------------------------

#     df_exam_subject= pd.read_csv('exam_with_subject.csv')
#     # print(df_exam_subject)
#     list1 = [""] * len(df_exam_subject)
#     df_exam_subject["correct sequence present"] = list1
#     for ind in df_exam_subject.index:
#        # if df_exam_subject['exam'][ind]=='11th CBSE':
#         df_video_sequence=pd.read_csv('video_sequence.csv')
#         df_top_videos=pd.read_csv('TopVideos.csv')
#         exam=df_exam_subject['exam'][ind]
#         goal=df_exam_subject['goal'][ind]
#         subject=df_exam_subject['subject'][ind]
#         print(exam,goal,subject)


#         df_video_sequence = df_video_sequence[df_video_sequence['Exam'].str.contains(exam)]

#         df_video_sequence = df_video_sequence[df_video_sequence['Goal'].str.contains(goal)]
#         # print(df_video_sequence)
#         df_video_sequence = df_video_sequence[df_video_sequence['Subject'].str.contains(subject)]


#         df_top_videos=df_top_videos[df_top_videos['exam'].str.contains(exam)]
#         df_top_videos =df_top_videos[df_top_videos['goal'].str.contains(goal)]
#         df_top_videos =df_top_videos[df_top_videos['subject'].str.contains(subject)]

#         # print(df_top_videos)
#         # print(df_video_sequence)
#         df_top_videos=df_top_videos[['videoId']]
#         df_video_sequence=df_video_sequence[['Id']]
#         # df_top_videos['videotitle'] = df_top_videos['videotitle'].str.upper() 
#         # df_video_sequence['Title'] = df_video_sequence['Title'].str.upper() 
#         print(df_video_sequence)
#         print(df_top_videos)

#         cond = df_video_sequence['Id'].isin(df_top_videos['videoId'])
# #
#         df_video_sequence.drop(df_video_sequence[cond].index, inplace = True)
#         print(df_video_sequence)
#         if len(df_video_sequence)==0:
#             df_exam_subject["correct sequence present"][ind]='yes'
#         else:

#             df_exam_subject["correct sequence present"][ind]='no'

#         df_exam_subject.to_csv('exam_with_subject.csv',index=False)  
#         print(df_exam_subject["correct sequence present"][ind]  )
#        # else :
#        #  continue


        

#     
