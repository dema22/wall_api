from sendgrid import Email, To, Content, Mail, sendgrid


def send_emails(request):
    sg = sendgrid.SendGridAPIClient('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')
    from_email = Email('felipedemaria@hotmail.com')
    to_email = To(request.data['email'])
    subject = 'Welcome to the Wall App !'
    message = f'Hi {request.data["username"]}!\n You have joined The Wall community! Have Fun!!'
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)
    # Using the sg api to send our email
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)