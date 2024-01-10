import smtplib
from core.config import *
from core.logger import logger


def send_email(receiver, subject, content):
    message = f"""
    From: From WorkClock team <{SMTP_SENDER}>
    To: To Person <{receiver}>
    Subject: {subject}

    {content}
    """.strip()

    try:
        smtp_object = smtplib.SMTP(SMTP_HOST)
        smtp_object.sendmail(SMTP_SENDER, receiver, message)
        logger.info(f'Successfully sent email to {receiver}\nContent: {content}')
    except Exception as ex:
        logger.error(f"Error: unable to send email to {receiver}\n{str(ex)}")

