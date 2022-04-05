from re import L
import pandas as pd
from pprint import pprint


def parse(excel_path="FINA-TOPDF.xlsx"):
	student_records = pd.read_excel(excel_path)

	
	id_grand = {}

	for i, row in student_records.iterrows():


		# print(student_efc)
		if row['ID_NUM'] not in id_grand.keys():

			id_grand[row['ID_NUM']] = { "first_name": row['FIRST_NAME'],
												"last_name": row['LAST_NAME'],
												"aids": {
														"Scholarship": [0],
														"Pell Grant": [0],
														"Sub_lone": [0],
														"Unsub_lone": [0]}
														}

		if "Scholarship" in row["value"]:
			id_grand[row['ID_NUM']]["aids"]['Scholarship'].append(row["award_amount"])
		elif "Pell" in row["value"]:
			id_grand[row['ID_NUM']]["aids"]['Pell Grant'].append(row["award_amount"])
		elif "DLSUB" in row["code"]:
			id_grand[row['ID_NUM']]["aids"]['Sub_lone'].append(row["award_amount"])
		elif "DLUNSUB" in row["code"]:
			id_grand[row['ID_NUM']]["aids"]['Unsub_lone'].append(row["award_amount"])



	
	return id_grand	


if __name__ == '__main__':
	parse()


