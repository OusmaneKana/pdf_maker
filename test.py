from pypdf import PdfReader, PdfWriter
import qrcode
import os, io
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape



reader = PdfReader("template.pdf")
writer = PdfWriter()

page1 = reader.pages[0]
page2= reader.pages[1]
fields = reader.get_fields()


writer.add_page(page1)
writer.add_page(page2)


""" THE Following fields are to be updated:
    - On page 1:

        * student_name1
        * phrase_acceptance (Congratulations on ...... with major and year)
    - On page 2:
        DIRECT COSTS
        * tuitionAndFee
        * housingFee
        * mealPlanFee
        * athleticsFee
        * totalDirectCost

        FINANCIAL AID
        * institutionalScholarship
        * pellGrant
        * directSubLoan
        * directUnsubLoan
    *
    *
"""

shippping_info = {"student_name":"Serigne Ciss",
                   "street_address":" 2525 City WestBld",
                    "city_zip":"Hosuton 77477" }



financial_aid  = {
        "institutionalScholarship": 6500,
        "pellGrant": 1200,
        "directSubLoan": 2500,
        "directUnsubLoan": 453}


direct_cost_dct= {
        "tuitionAndFee": 6540,
        "housingFee": 1800,
        "mealPlanFee": 1440,
        "athleticsFee": 900}

total_direct_cost = sum([val for key,val in direct_cost_dct.items()])
total_aid = sum([val for key,val in financial_aid.items()])



writer.update_page_form_field_values(
    writer.pages[0], {
                        "address_name":shippping_info["student_name"],
                        "address_street":shippping_info["street_address"],
                        "address_city_zip":shippping_info["city_zip"],
        
                        "student_name1": shippping_info["student_name"],
                      "phrase_acceptance": "Congratulation on your acceptance for our Bachelors of Science in Computer Science for the Fall Semester 2023"}
)


writer.update_page_form_field_values(
    writer.pages[1], {
        "tuitionAndFee": "$"+str(direct_cost_dct["tuitionAndFee"]),
        "housingFee": "$"+str(direct_cost_dct["housingFee"]),
        "mealPlanFee": "$"+str(direct_cost_dct["mealPlanFee"]),
        "athleticsFee": "$"+str(direct_cost_dct["athleticsFee"]),
        "totalDirectCost": "$"+str(total_direct_cost),

        
        "institutionalScholarship": "$"+str(financial_aid["institutionalScholarship"]),
        "pellGrant": "$"+str(financial_aid["pellGrant"]),
        "directSubLoan": "$"+str(financial_aid["directSubLoan"]),
        "directUnsubLoan": "$"+str(financial_aid["directUnsubLoan"]),
        "totalAid": "$"+str(total_aid),

        "balanceString": "Balance" if total_direct_cost>total_aid else "Refund",
        "balanceAmount": "$"+str(abs(total_direct_cost - total_aid)),
        },
)

# write "output" to PyPDF2-output.pdf
with open("filled-out1.pdf", "wb") as output_stream:
    writer.write(output_stream)


def generate_qr():
    
    # Data to encode
    data = "https://fs.na.edu"
    
    # Creating an instance of QRCode class
    qr = qrcode.QRCode(version = 1,
                    box_size = 10,
                    border = 5)
    
    # Adding data to the instance 'qr'
    qr.add_data(data)
    
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'black',
                        back_color = 'white')
    
    img.save('qr_code.png')

def add_image():
 
   
    in_pdf_file = 'filled-out1.pdf'
    out_pdf_file = 'filled-out1.pdf'
    img_file = 'qr_code.png'
 
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=landscape(letter))
    #can.drawString(10, 100, "Hello world")
    x_start = 630
    y_start = -120
    can.drawImage(img_file, x_start, y_start, width=120, preserveAspectRatio=True, mask='auto')
    can.showPage()
    can.showPage()
    can.showPage()
    can.save()
 
    #move to the beginning of the StringIO buffer
    packet.seek(0)
 
    new_pdf = PdfReader(packet)
 
    # read the existing PDF
    existing_pdf = PdfReader(open(in_pdf_file, "rb"))
    output = PdfWriter()

    output.add_page(existing_pdf.pages[0])

    #create page with QR
    page = existing_pdf.pages[1]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

 
    outputStream = open(out_pdf_file, "wb")
    output.write(outputStream)
    outputStream.close()


generate_qr()
add_image()