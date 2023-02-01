from reportlab.pdfgen import canvas
from reportlab.lib.colors import magenta, pink, blue, green, red, black
from reportlab.lib.pagesizes import letter, landscape
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfname import PdfName

import pdfrw 
from pypdf import PdfWriter, PdfReader

from pdfrw.objects.pdfstring import PdfString
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfarray import PdfArray

from reportlab.lib.units import mm, inch
import datetime, sys, io
import pandas as pd
from pprint import pprint
import excel_parser
import math

def main(): 
    student_record = excel_parser.parse() # Is a dictionary
    FA_data = excel_parser.parse_FA_data() # Is a dictionarie


    ite = 0


    for student_id, data in student_record.items():
        efc = student_record[student_id]['aids']['efc']

        for key, value in FA_data.items(): # From the FA_data dictionary match the record with the efc to get the Pell Grant amount.
            
            try:
                if key[0]<=efc<=key[1]:
                    
                    student_record[student_id]['aids']['pell_grant'] = value
                    break
                else:
                    
                    student_record[student_id]['aids']['pell_grant'] = 0
                    break
            except Exception as e:
                
                student_record[student_id]['aids']['pell_grant'] = 0
                 # break

   

    for student_id, record in student_record.items():

        total_scholarship = 0 if math.isnan(record['aids']['total_scholarship']) else int(record['aids']['total_scholarship'])
        pell_grant = 0 if math.isnan(record['aids']['pell_grant']) else int(record['aids']['pell_grant'])

        sub_loan = 0 if math.isnan(record['aids']['sub_loan']) else int(record['aids']['sub_loan'])
        unsub_loan = 0 if math.isnan(record['aids']['unsub_loan']) else int(record['aids']['unsub_loan'])


        total_aid = sum([total_scholarship//2,
                         pell_grant,
                        sub_loan//2,
                        unsub_loan//2,


                         ])
       
        
        # print(record)
        file_name = create_pdf(student_id, record)
        javascript_added = append_js_to_pdf(file_name,total_aid)
        ite+=1
       


def make_js_action(js):
    action = PdfDict()
    action.S = PdfName.JavaScript
    action.JS = js
    return action

def create_pdf(student_id, record): 


    template = "1117_template.pdf"
    file_name = f"C:/Users/umcr/OneDrive - North American University/S.A/FA Pdfs/Fall 2023/{record['full_name'].strip()}.pdf"
    # file_name = f"pdf_outputs/{record['full_name'].strip()}.pdf"

    # file_name = "test_output.pdf"

    total_scholarship = 0 if math.isnan(record['aids']['total_scholarship']) else int(record['aids']['total_scholarship'])
    pell_grant = 0 if math.isnan(record['aids']['pell_grant']) else int(record['aids']['pell_grant'])

    sub_loan = 0 if math.isnan(record['aids']['sub_loan']) else int(record['aids']['sub_loan'])
    unsub_loan = 0 if math.isnan(record['aids']['unsub_loan']) else int(record['aids']['unsub_loan'])


    



    packet = io.BytesIO()
    c = canvas.Canvas(packet,pagesize=landscape(letter))

    c.drawString(110, 507, record['full_name'])

    c.drawString(110, 491, str(int(student_id)))



    
    c.drawString(600, 387, "${:,}".format(total_scholarship//2)) #Divided by 2 because input price is yearly


    if pell_grant//2 > 1:
        c.drawString(600, 353, "${:,}".format((pell_grant)+1)) 
    else:
        c.drawString(600, 353, "${:,}".format(pell_grant)) 

   
    c.drawString(600, 321, "${:,}".format(sub_loan//2))  #Divided by 2 because input price is yearly

    c.drawString(600, 289, "${:,}".format(unsub_loan//2))  #Divided by 2 because input price is yearly


    c.save()
    

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfReader(packet)
    # read your existing PDF
    existing_pdf = PdfReader(template)
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    # finally, write "output" to a real file
    outputStream = open(file_name, "wb")
    output.write(outputStream)
    outputStream.close()

    return file_name


def append_js_to_pdf(file_name, total_aid = 0):

    pdf_writer = pdfrw.PdfWriter()
    pdf_reader = pdfrw.PdfReader(file_name)
    try:
      js = open("calculator.js").read().replace("total_aid_here",str(total_aid))
    except Exception as e:
      print(e)
      print("JS NOT FOUND")
      # js = "app.alert('HOLA!');"
      js = ""
    for page_index in pdf_reader.pages:
        page = page_index
        page.Type = PdfName.Page
        for field in page.Annots:
            try:
                if field['/T'].replace(")", "").replace("(","") in ["tuitionAndFee","athleticsFee","ownResources", "housingFee", "mealPlan"] :
                    field.update(PdfDict(AA=PdfDict(Bl=make_js_action(js))))
            except AttributeError:
                continue
        page.AA = PdfDict()
        page.AA.O = make_js_action(js)
        pdf_writer.addpage(page)  
    pdf_writer.write(file_name)

if __name__ == "__main__":
    main() 

