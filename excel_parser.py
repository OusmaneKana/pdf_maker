from re import L
import pandas as pd
from pprint import pprint



def parse_FA_data():
	pell_grant_amounts = pd.read_excel("bin/transformed_data.xlsx", sheet_name=0)

	efc_dct = {}
	# print(pell_grant_amounts.head())
	for column in pell_grant_amounts:
		efc_dct[pell_grant_amounts[column][0], pell_grant_amounts[column][2]] = pell_grant_amounts[column][3]

		


	return efc_dct
def parse():
	excel_path="bin/student_records_pr.xlsx"
	
	student_records = pd.read_excel(excel_path)

	
	id_grand = {}

	for i, row in student_records.iterrows():


		# print(student_efc)
		if row['Jenzabar ID'] not in id_grand.keys():

			id_grand[row['Jenzabar ID']] = { "full_name": row['Name'],
												
												"aids": {
														"efc": row["EFC"],
														"dependency_status": row["Dependency Status (D/I)"],
														"sub_loan": row["Sub Loan"],
														"unsub_loan": row["Unsub Loan"],
														"total_scholarship": row["Total Scholarship"]}
														}

	return id_grand	


if __name__ == '__main__':
	parse_FA_data()


