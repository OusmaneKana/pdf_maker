from tkinter import *
import acroform_pdf_new
from tkinter import messagebox

def generate():
	acroform_pdf_new.main()
	messagebox.showinfo( "Alert" , "Done Updating Pdfs" )



window=Tk()
btn=Button(window, text="Generate Pdfs", fg='blue', command = generate)
btn.place(x=80, y=100)

close_btn=Button(window, text="Close App", fg='red', command = window.destroy)
close_btn.place(x=80, y=150)
# lbl=Label(window, text="Click the Button to Generate New PDfs", fg='red', font=("Helvetica", 16))
# lbl.place(x=60, y=50)

window.title('NAU F.A Pdf Maker')
window.geometry("300x200+10+10")
window.mainloop()