from reportlab.pdfgen import canvas
from reportlab.lib.colors import magenta, pink, blue, green, red, black
from reportlab.lib.pagesizes import letter, landscape
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfname import PdfName
from pdfrw import PdfReader, PdfWriter
from pdfrw.objects.pdfstring import PdfString
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfarray import PdfArray
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.units import mm, inch
import datetime, sys, io
import pandas as pd
from pprint import pprint
import excel_parser

def main(): 

    #DEFAUTL ARGUMENT OF PDF PARSER IS EXCEL THAT I USED, YOU CAN OVERWRITE IT WITH YOUR EXCEL NAME OR CHANGE THE DEFAULT NAME ON excelparser,py
    student_record = excel_parser.parse()


    # print(type(student_record))
    ite = 0
    for student_id, record in student_record.items():

        if sum(record['aids']['Pell Grant'])//2 > 1:

            pell_grant = (sum(record['aids']['Pell Grant'])//2 )+1
        else:
            pell_grant = sum(record['aids']['Pell Grant'])//2


        total_aid = sum([sum(record['aids']['Scholarship'])/2,
                         pell_grant,
                        sum(record['aids']['Sub_lone'])//2,
                        sum(record['aids']['Unsub_lone'])//2

                         ])
       
        if ite ==1:
            break
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

    # pprint(record)



    template = "1117_template.pdf"
    file_name = f"pdf_outputs/{record['first_name']} {record['last_name']}.pdf"
    # file_name = "test_output.pdf"



    packet = io.BytesIO()
    c = canvas.Canvas(packet)

    c.drawString(110, 507, record['last_name']+ "," +record['first_name'])

    c.drawString(110, 491, str(student_id))
    
    c.drawString(600, 387, "${:,}".format(sum(record['aids']['Scholarship'])//2)) #Divided by 2 because input price is yearly

    if sum(record['aids']['Pell Grant'])//2 > 1:
        c.drawString(600, 353, "${:,}".format((sum(record['aids']['Pell Grant'])//2)+1)) 
    else:
        c.drawString(600, 353, "${:,}".format(sum(record['aids']['Pell Grant'])//2)) 

   
    c.drawString(600, 321, "${:,}".format(sum(record['aids']['Sub_lone'])//2))  #Divided by 2 because input price is yearly

   
    c.drawString(600, 289, "${:,}".format(sum(record['aids']['Unsub_lone'])//2))  #Divided by 2 because input price is yearly


    c.save()
    

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(template, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(file_name, "wb")
    output.write(outputStream)
    outputStream.close()

    return file_name


def append_js_to_pdf(file_name, total_aid = 0):

    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(file_name)
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

