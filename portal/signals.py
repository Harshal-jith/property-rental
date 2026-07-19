from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Booking

@receiver(pre_save, sender=Booking)
def store_original_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._original_status = Booking.objects.get(pk=instance.pk).status
        except Booking.DoesNotExist:
            instance._original_status = None
    else:
        instance._original_status = None

@receiver(post_save, sender=Booking)
def send_booking_status_email(sender, instance, created, **kwargs):
    recipient_name = instance.user.full_name or 'Valued Customer'
    
    try:
        if created:
            # 1. Booking Submitted confirmation
            subject = f"Booking Request Submitted: {instance.property.title}"
            context = {
                'booking': instance,
                'recipient_name': recipient_name,
            }
            html_message = render_to_string('portal/emails/booking_submitted.html', context)
            plain_message = strip_tags(html_message)
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                html_message=html_message,
                fail_silently=False,
            )
        else:
            old_status = getattr(instance, '_original_status', None)
            if old_status and old_status != instance.status:
                # 2. Booking Status Changed (Approved or Rejected)
                subject = f"Booking Request Update: {instance.property.title} - {instance.status}"
                context = {
                    'booking': instance,
                    'recipient_name': recipient_name,
                }
                if instance.status == 'Approved':
                    template = 'portal/emails/booking_approved.html'
                else:
                    template = 'portal/emails/booking_rejected.html'

                html_message = render_to_string(template, context)
                plain_message = strip_tags(html_message)
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.email],
                    html_message=html_message,
                    fail_silently=False,
                )
    except Exception as e:
        print(f"Error sending confirmation email to {instance.email}: {e}")
