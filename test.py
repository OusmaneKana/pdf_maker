from pypdf import PdfWriter, PdfReader
# import StringIO
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
# packet = StringIO.StringIO()
packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(100,100, "Hello world")
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfReader(packet)
# read your existing PDF
existing_pdf = PdfReader("1117_template.pdf", "rb")
output = PdfWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
# finally, write "output" to a real file
outputStream = "newpdf.pdf"
output.write(outputStream)
