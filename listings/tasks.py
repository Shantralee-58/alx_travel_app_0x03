from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation(email, booking_details):
    subject = 'Booking Confirmation'
    message = f"Hello! Your booking is confirmed. Details: {booking_details}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return True

