import smtplib
from email.mime.text import MIMEText

def send_violation_email(number_plate):
    sender_email = "hackhustlerssender@gmail.com"
    receiver_email = "kmariandeepak@gmail.com"
    subject = "Traffic Violation Alert"
    body = f"Helmet violation detected! Vehicle number: {number_plate}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, "hackhustlers@26")
        server.sendmail(sender_email, receiver_email, msg.as_string())