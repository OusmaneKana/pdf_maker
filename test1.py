from PyPDF2 import PdfWriter, PdfReader

output = PdfWriter()
ipdf = PdfReader(open('template.pdf', 'rb'))

page = ipdf.pages[0]
output.add_page(page)

with open('new.pdf', 'wb') as f:
    output.add_js('this.getField("student_name1").value = "$first_name"')
    output.write(f)