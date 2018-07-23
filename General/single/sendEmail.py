from pimThor3.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def sendMail(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False
    )