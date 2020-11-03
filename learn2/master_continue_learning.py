
from home_data_continue_learning import home_data
import pandas as pd


if __name__ == '__main__':

    df = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",'Type', 'Id', "Title", "Subject", "Subject_tagged"])
    df.to_csv("continue_learning.csv")

    df1=pd.read_csv("actual_continue_learning.csv")
    home_data()
    df2=pd.read_csv("continue_learning.csv")

    for ind in df1.index:
        list1 = [""] * len(df1)
        df1["present in api"] = list1
        df_new=df2.loc[df2["Id"]==df1["Id"][ind]]
        if len(df_new)==1:
            df1["present in api"][ind]="yes"
        else:
            df1["present in api"][ind] = "no"
        df1.to_csv("actual_continue_learning.csv",index=False)


