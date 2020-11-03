import pandas as pd
def get_chapter_of_exam(exam,df1):
    return df1[df1['Exam'].str.contains(exam)]

def chapter_correctly_present(exam,id):
    df=pd.read_csv("chapter_data.csv")

    df = df.loc[df["Chapter Id"] == id]

    #     print(df)

    if len(df) == 0:
        return "NA"
    else:
        df = get_chapter_of_exam(exam, df)
        if len(df) > 0:
            return "Yes"
        else:
            return "No"
