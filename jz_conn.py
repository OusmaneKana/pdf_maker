
import pymysql.cursors
import pymssql
import pandas
from pprint import pprint
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")


def get_records():
    conn = pymssql.connect(server=CONFIG['server'], user=CONFIG['user'],
                           password=CONFIG['password'], database=CONFIG['database'])
    cursor = conn.cursor()

    records = cursor.execute("""
                select  bm.ssn,bm.ID_NUM, nm.FIRST_NAME, nm.LAST_NAME, ap.award_year_id, ap.award_amount, att.code, att.value, nms.EMAIL_ADDRESS, convert(date, bm.BIRTH_DTE) as 'BIRTH_DTE'
                from[JZNAT-SQL1].[J1FALIVE].[ngp].student_award_package ap
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].[award_type] att on att.id = ap.award_type_id
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].financial_aid_year fy on fy.id = ap.financial_aid_year_id
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].person p on p.id = ap.constituent_id
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].award_status_type awstp on awstp.id = att.award_status_type_id
                inner join [JZNAT-SQL1].[J1PRD].[dbo].[BIOGRAPH_MASTER] bm on p.social_security_number = bm.SSN
                inner join  [JZNAT-SQL1].[J1PRD].[dbo].[NAME_MASTER] nm on nm.ID_NUM = bm.ID_NUM
                inner join  [JZNAT-SQL1].[J1PRD].[dbo].[NAME_AND_ADDRESS] nms on nms.ID_NUM = bm.ID_NUM
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].verify_isir ni on ni.constituent_id = p.id
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].isir_ver_status_type nt on nt.id = ni.isir_ver_status_type_id
                where ap.award_year_id = 9 and ni.award_year_type_id = 9
                order by ap.created_on asc
                """)


    records = cursor.fetchall()

    records_df = pandas.DataFrame(records)
    records_df.columns = [
        "SSN",
        "Student ID",
        "First Name",
        "Last Name",
        "Award Year",
        "Award Amount",
        "Code",
        "Value",
        "Email",
        "Birthday"
      
        ]
    # new_header = records_df.iloc[0]
    # records_df = records_df[1:]

    # print(records_df.head())

    records_df["SSN"] = records_df["SSN"].apply(lambda x: str(x)[5:])
    id_grand = {}

    for i, row in records_df.iterrows():

        # print(student_efc)
        if row['SSN'] not in id_grand.keys():

            id_grand[row['SSN']] = {
                                    "actual_id":row['Student ID'],
                                    "first_name": row['First Name'],
                                    "birthdate": row["Birthday"],
                                    "last_name": row['Last Name'],
                                     "aids": {
                                                "Scholarship": [0],
                                                "Pell Grant": [0],
                                                "Sub_lone": [0],
                                                 "Unsub_lone": [0]},
                                    "email":row["Email"]
                                        }
        # Check codes
        scholarship_codes = ['BOARD', 'ECOHARD', "FOUNDATION","HARMONY","NAU","PROVOST","STAFFORD",]
        # print(row["Value"])
        if row["Code"].strip() in scholarship_codes:
           
            id_grand[row['SSN']]["aids"]['Scholarship'].append(
                float(row["Award Amount"]))
        elif "PELL" in row["Code"]:
            id_grand[row['SSN']]["aids"]['Pell Grant'].append(
                float(row["Award Amount"]))
        elif "DLSUB" in row["Code"]:
            id_grand[row['SSN']]["aids"]['Sub_lone'].append(
                float(row["Award Amount"]))
        elif "DLUNSUB" in row["Code"]:
            id_grand[row['SSN']]["aids"]['Unsub_lone'].append(
                float(row["Award Amount"]))

  
    return id_grand


if __name__ == "__main__":
    pprint(get_records())
