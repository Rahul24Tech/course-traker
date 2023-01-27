from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from playlist import settings


@shared_task(bind=True)
def send_mail_func(self):
    """
    This function is used to send email notification in background.
    """
    mail_subject = "Hye from celery"
    message = "Yaaaa....I have Added course by celery!!"
    to_email = "test@yopmail.com"
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )
    return "Done"
