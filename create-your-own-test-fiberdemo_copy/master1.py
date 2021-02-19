import pandas as pd
from atg_create_test import ATG_test
from goal_exam_extractor import goal_exam_grade_extractor
from progress_checker import progress_check
import time

df = goal_exam_grade_extractor()
df=pd.read_csv('test_file2.csv')
df1 = pd.DataFrame(
    columns=["Exam", "Goal", "Exam_code", 'Time', 'Name', 'Incorrect_marks', 'Correct_marks', 'Difficulty',
             'Section_data',
             'Chapter_data', 'Atg_id', 'Request_id', 'Success', 'Progress', "Subject","ATG payload","Embibe-token"])
df1.to_csv('Create_test_data.csv', index=False)
for ind in df.index:
    # if df["Exam_name"][ind]=="CTET Paper 1":
        ATG_test(df["Goal"][ind], df["Exam_name"][ind], df["Exam_code"][ind])
        # break
# else:
# continue
time.sleep(120)

# for i in range(0, 10000000):
progress_check(pd.read_csv('Create_test_data.csv'))
df=pd.read_csv('Create_test_data.csv')
df.to_excel('Create_test_data.xlsx',index=False)
# update_sheet('Create_test_data','Sheet1')
    # print(i)
    # if progress == 30:
    #     break
    # else:
    #     print(progress)
    #     continue
