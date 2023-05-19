from reportlab.pdfgen import canvas
from reportlab.lib.colors import magenta, pink, blue, green, red, black
from reportlab.lib.pagesizes import letter, landscape
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfstring import PdfString
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfarray import PdfArray
from pypdf import PdfWriter, PdfReader
import pdfrw
from reportlab.lib.units import mm, inch
import datetime, sys, io
import pandas as pd
from pprint import pprint

import jz_conn





def main(): 
    # student_record = excel_parser.parse()
    student_record = jz_conn.get_records()


    # print(type(student_record))
    ite = 0
    for student_id, record in student_record.items():

        # if ite ==1:break

        if sum(record['aids']['Pell Grant'])//2 > 1:

            pell_grant = (sum(record['aids']['Pell Grant'])//2)+1
        else:
            pell_grant = sum(record['aids']['Pell Grant'])//2


        total_aid = sum([sum(record['aids']['Scholarship'])/2,
                         pell_grant,
                        sum(record['aids']['Sub_lone'])//2,
                        sum(record['aids']['Unsub_lone'])//2

                         ])
       
        
        # print(record)
        file_name = create_pdf(record)
        javascript_added = append_js_to_pdf(file_name,total_aid)
        ite+=1


def make_js_action(js):
    action = PdfDict()
    action.S = PdfName.JavaScript
    action.JS = js
    return action

def create_pdf(record): 

    # pprint(record)



    template = "1117_template.pdf"
    file_name = f"C:/Users/umcr/OneDrive - North American University (1)/S.A/FA Pdfs/Fall 2023/{record['first_name'].strip()} {record['last_name'].strip()}.pdf"
    
    # file_name = f"pdf_outputs/{record['first_name'].strip()} {record['last_name'].strip()}.pdf"

    # file_name = "test_output.pdf"



    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=landscape(letter))

    c.drawString(110, 507, record['last_name']+ "," +record['first_name'])

    c.drawString(110, 491, str(record['actual_id']))
    
    c.drawString(600, 387, "${:,}".format(int(sum(record['aids']['Scholarship'])//2))) #Divided by 2 because input price is yearly

    if sum(record['aids']['Pell Grant'])//2 > 1:
        c.drawString(600, 353, "${:,}".format(int((sum(record['aids']['Pell Grant'])//2)+1))) 
    else:
        c.drawString(600, 353, "${:,}".format(int(sum(record['aids']['Pell Grant'])//2)))

   
    c.drawString(600, 321, "${:,}".format(int(sum(record['aids']['Sub_lone'])//2)))  #Divided by 2 because input price is yearly

   
    c.drawString(600, 289, "${:,}".format(int(sum(record['aids']['Unsub_lone'])//2)))  #Divided by 2 because input price is yearly


    c.save()
    

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfReader(packet)
    # read your existing PDF
    existing_pdf = PdfReader(open(template, "rb"))
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

