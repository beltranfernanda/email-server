import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config.config import Config
from app.exception.email_internal_error_exception import EmailInternalErrorException

__all__ = ['EmailService']


class EmailService:
    _subject: str = 'Private message from {name} in Maria personal webpage'

    def __init__(self, config: Config):
        self.config = config

    def send_message(self, name: str, email: str, phone: str, message: str) -> None:
        try:

            with (smtplib.SMTP(self.config.get_param('SMTP_SERVER'), int(self.config.get_param('SMTP_PORT')))
                  as server):
                formatted_message = self._format_message(name, email, phone, message)
                subject = self._subject.format(name=name)
                message = self._create_email(formatted_message, subject)
                server.starttls()
                server.login(self.config.get_param('EMAIL_USERNAME'), self.config.get_param('EMAIL_PASSWORD'))
                server.sendmail(self.config.get_param('SENDER_EMAIL'), self.config.get_param('RECIPIENT_EMAIL'),
                                message.as_string())
                server.close()

        except (smtplib.SMTPHeloError, smtplib.SMTPAuthenticationError, smtplib.SMTPNotSupportedError,
                smtplib.SMTPException, smtplib.SMTPSenderRefused, smtplib.SMTPRecipientsRefused,
                smtplib.SMTPDataError) as err:

            error_message = f"An error has occurred sending the message: {err}"
            raise EmailInternalErrorException(error_message)

    def _format_message(self, name: str, email: str, phone: str, message: str) -> str:
        with open(os.path.join(os.getcwd(), "app", "template", "mail.html"), "r") as file:
            html_content = file.read()

        formatted_html_content = html_content.format(name_sender=name,
                                                     phone_number=phone,
                                                     email_sender=email,
                                                     email_message=message)
        return formatted_html_content

    def _create_email(self, formatted_body, subject) -> MIMEMultipart:
        _message = MIMEMultipart()
        _message['From'] = self.config.get_param('SENDER_EMAIL')
        _message['To'] = self.config.get_param('RECIPIENT_EMAIL')
        _message['Subject'] = subject
        _message.attach(MIMEText(formatted_body, 'html'))
        return _message
