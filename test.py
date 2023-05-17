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
from string import Template

import jz_conn


def main():
    append_js_to_pdf("letter_template_test.pdf")
def append_js_to_pdf(file_name, total_aid = 0):

    pdf_writer = pdfrw.PdfWriter()
    pdf_reader = pdfrw.PdfReader(file_name)
    try:
        #   js = open("letter_filler.js").read()
        js = Template(open("letter_filler.js").read())
        js = js.substitute(    
                first_name = "Papi Munano",
    
                acceptance_phrase = f"Congratulations on your acceptance to Bachelor's of Science 2023 at North American University."
        )


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


def make_js_action(js):
    action = PdfDict()
    action.S = PdfName.JavaScript
    action.JS = js
    return action

if __name__ == "__main__":
    main()