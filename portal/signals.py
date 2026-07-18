from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

@receiver(post_save, sender=Booking)
def send_booking_status_email(sender, instance, created, **kwargs):
    if created:
        subject = "Booking Request Received"
        body = f"""Hello {instance.user.full_name},

Thank you for requesting to book **{instance.property.title}**.

Your booking request has been received successfully.

Current Status:
Pending

Our team or the property owner will contact you shortly.

Thank you for choosing our Property Rental Portal."""
    else:
        # Only send update email if it was triggered after creation (so status could be changed to Approved/Rejected)
        subject = f"Booking Status Update: {instance.status}"
        body = f"""Hello {instance.user.full_name},

There has been an update regarding your booking request for {instance.property.title}.

Current Status:
{instance.status}

Thank you for choosing our Property Rental Portal."""

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending confirmation email to {instance.email}: {e}")
