import smtplib
from core.config import *
from core.logger import logger


def send_email(receiver, subject, content):
    if not SMTP_SENDER or not SMTP_PASSWORD:
        logger.warning('SMTP_SENDER or SMTP_PASSWORD not set, email will not be sent')
        return
    
    message = f"""
    From: From WorkClock team <{SMTP_SENDER}>
    To: To Person <{receiver}>
    Subject: {subject}

    {content}
    """.strip()

    try:
        smtp_object = smtplib.SMTP('smtp-mail.outlook.com', 587)
        smtp_object.starttls()
        smtp_object.login(SMTP_SENDER, SMTP_PASSWORD)
        smtp_object.sendmail(SMTP_SENDER, receiver, message)
        logger.info(f'Successfully sent email to {receiver}\nContent: {content}')
    except Exception as ex:
        logger.error(f"Error: unable to send email to {receiver}\n{str(ex)}")

