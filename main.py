import pandas as pd

df = pd.read_csv('question_details.csv')
df1 = pd.read_csv('OT and Mockbank Qn ids (1).csv')
df1.insert(2, "Present in CG in published state", '')
for ind in df1.index:
    #print(df1['question_id'][ind])
    df_new = df.loc[df['id'] == df1['question_id'][ind]]

    if len(df_new) > 0:
        df1['Present in CG in published state'][ind] = 'Yes'
    else:
        df1['Present in CG in published state'][ind] = 'No'
   
df1.to_csv('OT_MB_questions_status_in_CG.csv',index=False)
