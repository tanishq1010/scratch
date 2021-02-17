from glob import glob
import pandas as pd


def produceOneCSV(list_of_files, file_out):
    result_obj = pd.concat([pd.read_excel(file) for file in list_of_files])
    result_obj.to_excel(file_out, index=False, encoding="utf-8")


list_of_files = [file for file in glob('Results/*.xlsx')]
print(list_of_files)

file_out = "ConsolidateOutput.xlsx"
produceOneCSV(list_of_files, file_out)
df=pd.read_excel('ConsolidateOutput.xlsx')
df.drop_duplicates(inplace=True)
df.to_excel('output.xlsx',index=False)
