import pandas as pd

df1 = pd.read_csv("Part1.csv")
df2 = pd.read_csv("Part2.csv")
df2 = df2[['question_status', 'question_id']]
df1 = df1[['question_status', 'question_id']]
# print(df1)
# print(df2)
df_1 = pd.concat([df1, df2])

df3 = pd.read_csv("result1.csv")
df4 = pd.read_csv("result2.csv")
df5 = pd.read_csv("result3.csv")
df6 = pd.read_csv("result4.csv")
df_2 = pd.concat([df3, df4, df5, df6])

list1 = [""] * len(df_1)
df_1["Question live in CG"] = list1
i=0
for ind in df_1.index:
    print(i)
    # print(df_1["question_id"][ind])
    dfnew = df_2.loc[df_2["id"] == str(df_1["question_id"][ind])]
    if len(dfnew)>0:
        df_1["Question live in CG"][ind]="yes"
    else:
        df_1["Question live in CG"][ind] = "no"

    i+=1
df_1.to_csv("overall.csv")
