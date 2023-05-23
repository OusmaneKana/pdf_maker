from PyPDF2 import PdfWriter, PdfReader

output = PdfWriter()
ipdf = PdfReader(open('template.pdf', 'rb'))

for i in range(len(ipdf.pages)):
    page = ipdf.pages[i]
    output.add_page(page)

with open('new.pdf', 'wb') as f:
    output.add_js("alert('Fak you')")
    output.write(f)