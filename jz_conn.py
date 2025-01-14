import pymssql
import pandas
from pprint import pprint
from dotenv import dotenv_values
import json

CONFIG = dotenv_values(b"C:\Users\UMCR\Desktop\projects_repo\pdf_maker\.env")


def get_records():
    conn = pymssql.connect(server=CONFIG['server'], user=CONFIG['user'],
                           password=CONFIG['password'], database=CONFIG['database'])
    cursor = conn.cursor()

    records = cursor.execute("""
                select  bm.ssn,bm.ID_NUM, nm.FIRST_NAME, nm.LAST_NAME, ap.award_year_id, ap.award_amount, att.code, att.value, nms.EMAIL_ADDRESS, convert(date, bm.BIRTH_DTE) as 'BIRTH_DTE', nms.ADDR_LINE_1, nms.ADDR_STS, nms.CITY, nms.[STATE], nms.ZIP
                from[JZNAT-SQL1].[J1FALIVE].[ngp].student_award_package ap
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].[award_type] att on att.id = ap.award_type_id
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].financial_aid_year fy on fy.id = ap.financial_aid_year_id
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].person p on p.id = ap.constituent_id
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].award_status_type awstp on awstp.id = att.award_status_type_id
                inner join [JZNAT-SQL1].[J1PRD].[dbo].[BIOGRAPH_MASTER] bm on p.social_security_number = bm.SSN
                inner join  [JZNAT-SQL1].[J1PRD].[dbo].[NAME_MASTER] nm on nm.ID_NUM = bm.ID_NUM
                inner join  [JZNAT-SQL1].[J1PRD].[dbo].[NAME_AND_ADDRESS] nms on nms.ID_NUM = bm.ID_NUM
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].verify_isir ni on ni.constituent_id = p.id
                inner join [JZNAT-SQL1].[J1FALIVE].[ngp].isir_ver_status_type nt on nt.id = ni.isir_ver_status_type_id
                where ap.award_year_id = 11 and ni.award_year_type_id >= 11
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
        "Birthday",
        "Address_Line_1",
        "Address_street",
        "Address_City", 
        "Address_State",
        "Address_Zip"
      
        ]
    
    
    id_grand = {}

    for i, row in records_df.iterrows():

        # print(student_efc)
        if row['SSN'] not in id_grand.keys():

            id_grand[row['SSN']] = {
                                    "actual_id":row['Student ID'],
                                    "first_name": row['First Name'],
                                    "birthdate": row["Birthday"],
                                    "last_name": row['Last Name'],
                                    "Address_Line_1": row['Address_Line_1'],
                                    "Address_street": row['Address_street'],
                                    "Address_City": row['Address_City'], 
                                    "Address_State": row['Address_State'],
                                    "Address_Zip": row['Address_Zip'],
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



def get_meal_plan_records():
    
    conn = pymssql.connect(server='JZNAT-SQL1', user='NA\JAPI', password='AmirBjapi@23', database='J1PRD')

    cursor = conn.cursor()

    cursor.execute("""

                    select nm.ID_NUM,nm.LAST_NAME, nm.FIRST_NAME, sc.MEAL_PLAN
                    from STUD_LIFE_CHGS sc
                    inner join NAME_AND_ADDRESS nm on nm.ID_NUM = sc.ID_NUM
                    where sc.TRM_CDE = 'FA' and sc.YR_CDE = 2024 

                """)
    
    record = cursor.fetchall()

    df = pandas.DataFrame(record)

    df.rename(columns={0:"student_id",1:"last_name",2:"first_name",3:"meal_plan_type" }, inplace=True)

    meal_plan_records = df.to_dict(orient='records')


  
    return meal_plan_records





if __name__ == "__main__":
    
    records = get_meal_plan_records()

    print(records[0])


