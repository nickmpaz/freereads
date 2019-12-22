import email, smtplib, ssl, os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
load_dotenv()

subject = "convert"
body = ""
sender_email = os.environ["SENDER_EMAIL"]
sender_password = os.environ["SENDER_PASSWORD"]
receiver_email = os.environ["RECEIVER_EMAIL"]

def send_email(filelocation, filename, progress_bar=False):

    if progress_bar:
        progress_bar.message = "creating email..."
        progress_bar.progress = 0
        progress_bar.draw()

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    if progress_bar:
        progress_bar.message = "attaching %s..." % filename
        progress_bar.progress = 0.33
        progress_bar.draw()
    
    with open(filelocation, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    if progress_bar:
        progress_bar.message = "sending email to %s..." % receiver_email
        progress_bar.progress = 0.66
        progress_bar.draw()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, text)

    if progress_bar:
        progress_bar.message = "email has been sent ✔"
        progress_bar.progress = 1
        progress_bar.draw()
