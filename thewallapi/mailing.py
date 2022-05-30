import os

from sendgrid import Email, To, Content, Mail, sendgrid


def send_emails(data):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SG_KEY'))
    from_email = Email(os.environ.get('SG_FROM'))
    to_email = To(data['email'])
    subject = 'Welcome to the Wall App !'
    message = f'Hi {data["username"]}!\n You have joined The Wall community! Have Fun!!'
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)
    # Using the sg api to send our email
    sg.client.mail.send.post(request_body=mail.get())