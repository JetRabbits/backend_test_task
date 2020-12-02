import os

from flask_mail import Mail, Message

from app.functions import app

MAIL_SENDER = app.config['MAIL_SENDER']
MAIL_RECIPIENTS = app.config['MAIL_RECIPIENTS']
mail = Mail(app)


def send_email(subject, text_body, html_body, attachment_file_paths, content_type='text/csv'):
    message = Message(subject, sender=MAIL_SENDER, recipients=MAIL_RECIPIENTS)
    message.body = text_body
    message.html = html_body
    if attachment_file_paths is not None:
        for attachment_file_path in attachment_file_paths:
            with open(attachment_file_path, encoding='utf-8') as attachment_file:
                file_name = os.path.basename(attachment_file.name)
                content = str(attachment_file.read()).encode('utf-8')
                message.attach(file_name, content_type, content)
    mail.send(message)