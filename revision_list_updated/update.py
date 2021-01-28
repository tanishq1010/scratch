import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import csv
import gspread_dataframe as gd


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
		'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('apiautomation-5f15e583dede.json', scope)
client = gspread.authorize(creds)

gc = gspread.service_account(filename='apiautomation-5f15e583dede.json')

def update_sheet_by_df(file_id,df,wk_name):

	sheet = gc.open_by_key(file_id)
	worksheet = sheet.worksheet(wk_name)

	worksheet.clear()
	gd.set_with_dataframe(worksheet, df)

def get_sheet_to_df(file_id,worksheet_name):
	sheet = gc.open_by_key(file_id)
	worksheet = sheet.worksheet(worksheet_name)
	return gd.get_as_dataframe(worksheet)


	# return pd.DataFrame(worksheet.get_all_records())
def update_sheet(name1,name2):
	file_id='120n_czr3986STxKBk9h4FdEYCq1WQv-uuU0mwyLDr8s'
	df=pd.read_csv(f"{name1}.csv")
	update_sheet_by_df(file_id,df,name2)
