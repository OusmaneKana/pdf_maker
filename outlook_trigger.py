from tkinter import mainloop
import win32com.client
import acroform_pdf_new
import sched, time
s = sched.scheduler(time.time, time.sleep)




def listen(sc):
    print("Listening")
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6) # "6" refers to the index of a folder - in this case,
                                    # the inbox. You can change that number to reference
                                    # any other folder
    messages = inbox.Items

    # Restrict to message to the subject generate pdf

    messages = messages.Restrict("[Subject] = 'Generate pdf'")


    message = messages.GetLast()
    if message and message.Unread == True:
        print("Triggering pdf making")
        acroform_pdf_new.main()
        print(f"Sending confirmation email to {message.senderEmailAddress}")
        send_email(message.senderEmailAddress)
        message.Unread = False

    sc.enter(5, 1, listen, (sc,))
   

def send_email(recipient_email):
    outlook = win32com.client.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = recipient_email
    mail.Subject = "Automated Response DO NOT REPLY"
    mail.HTMLBody = """<h2>This is a conformation email</h2>
                    
                    <p> Your request has been received. New Pdfs have been posted
                        in <a href = "https://nau3203-my.sharepoint.com/:f:/g/personal/sciss_na_edu/EtbTiqN3tvBNlNts1k3ISJcBsrHgiv8JgdE024sgS0CKRg?e=AEVphM">This folder</a> 

                    <p> Please email jadmin@na.edu if you are encounterirng any issues </p>
                    """
  
    mail.Send()


s.enter(5, 1, listen, (s,))
s.run()