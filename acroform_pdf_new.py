from reportlab.pdfgen import canvas
from reportlab.lib.colors import magenta, pink, blue, green, red, black
from reportlab.lib.pagesizes import letter, landscape
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfdict import PdfDict
from pypdf import PdfWriter, PdfReader
import pdfrw
 
import io




import jz_conn





def main(): 
    # student_record = excel_parser.parse()
    student_record = jz_conn.get_records()


    # print(type(student_record))
    ite = 0
    for student_id, record in student_record.items():

        # if ite ==2:break

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

        createOfferLetter(record)

        # add_image_to_pdf(final_output_file)

        ite+=1



def make_js_action(js):
    action = PdfDict()
    action.S = PdfName.JavaScript
    action.JS = js
    return action

def create_pdf(record): 

    # pprint(record)

    template = "1117_template.pdf"
    file_name = f"C:/Users/UMCR/OneDrive - North American University/S.A/FA Pdfs/Spring 2024/{record['first_name'].strip()} {record['last_name'].strip()}.pdf"
    
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



def createOfferLetter(record):

    print("...... Creating Offer Letters ......")
    
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

    shippping_info = {"student_name":record['first_name'] +" " +record['last_name'],
                    "street_address":f"{record['Address_Line_1']}",
                        "city_zip":f"{record['Address_City']} {record['Address_State']} {record['Address_Zip']}"}



    financial_aid  = {
            "institutionalScholarship": int(sum(record['aids']['Scholarship']))//2,
            "pellGrant": int(sum(record['aids']['Pell Grant']))//2+1 if int(sum(record['aids']['Pell Grant']))//2 >1 else int(sum(record['aids']['Pell Grant']))//2,
            "directSubLoan": int(sum(record['aids']['Sub_lone']))//2,

            "directUnsubLoan": int(sum(record['aids']['Unsub_lone']))//2}


    direct_cost_dct= {
            "tuitionAndFee": 7718,
            "housingFee": 0,
            "mealPlanFee": 0,
            "athleticsFee": 0}

    total_direct_cost = int(sum([val for key,val in direct_cost_dct.items()]))
    total_aid = int(sum([val for key,val in financial_aid.items()]))



    writer.update_page_form_field_values(
        writer.pages[0], {
                            "address_name":shippping_info["student_name"],
                            "address_street":shippping_info["street_address"],
                            "address_city_zip":shippping_info["city_zip"],
            
                            "student_name1": shippping_info["student_name"]+",",
                        "phrase_acceptance": "Congratulation on your acceptance at North American University for the Fall Semester 2024! "}
    )


    writer.update_page_form_field_values(
        writer.pages[1], {
            "tuitionAndFee": "$"+str(direct_cost_dct["tuitionAndFee"]),
            "housingFee": "$ -",
            "mealPlanFee": "$ -",
            "athleticsFee": "$ -",
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

    # final_output_file = f"pdf_outputs/Offer Letters/{record['first_name'].strip()} {record['last_name'].strip()}.pdf"
    final_output_file =f"C:/Users/UMCR/OneDrive - North American University/S.A/FA Pdfs/Spring 2024/Offer Letters/{record['first_name'].strip()} {record['last_name'].strip()}.pdf"


    with open(final_output_file, "wb") as output_stream:
        writer.write(output_stream)
    
    print(f"Output filename {final_output_file}")
   




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

def add_image_to_pdf(in_pdf_file):

    out_pdf_file = in_pdf_file
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



if __name__ == "__main__":
    main() 

