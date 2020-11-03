import pandas as pd

df1 = pd.read_csv("Part1.csv")
df2 = pd.read_csv("Part2.csv")
df2 = df2[['question_status', 'question_id']]
df1 = df1[['question_status', 'question_id']]
# print(df1)
# print(df2)
df_1 = pd.concat([df1, df2])
df_1.to_csv("onlinetyari.csv",index=False)
df_1=pd.read_csv("onlinetyari.csv")
df3 = pd.read_csv("result1.csv")
df4 = pd.read_csv("result2.csv")
df5 = pd.read_csv("result3.csv")
df6 = pd.read_csv("result4.csv")
df_2 = pd.concat([df3, df4, df5, df6])
df_2.to_csv("CG_onlinetyari.csv",index=False)
df_2=pd.read_csv("CG_onlinetyari.csv")


df_1.drop_duplicates(inplace=True)
df_2.drop_duplicates(inplace=True)
# print(df_1)
# print(df_2)


list1 = [""] * len(df_2)
df_2["ID"] = list1
i=0
for ind in df_2.index:
    print(i)
    # int(df_2["id"][ind]))
    y=int(df_2["id"][ind])
    df_2["ID"][ind]=y
    # print(df_2["ID"][ind])
    i+=1
    # if i>20:
        # break



list1 = [""] * len(df_1)
df_1["Question live in CG"] = list1
i=0
for ind in df_1.index:
    print(i)
    # print(df_1["question_id"][ind])
    dfnew = df_2.loc[df_2["ID"] == int(df_1["question_id"][ind])]
    if len(dfnew)>0:
        df_1["Question live in CG"][ind]="yes"
    else:
        df_1["Question live in CG"][ind] = "no"

    i+=1
    df_1.to_csv("onlinetyari.csv")

