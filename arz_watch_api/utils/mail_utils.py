from django.conf import settings
from django.contrib.auth.models import User

from .email_thread import EmailThread


def async_notify_superusers(message: str):
    """Send an alert email to all active superusers asynchronously."""
    subject = "Arz Watch API Alert"

    superusers_emails = User.objects.filter(
        is_superuser=True, is_active=True
    ).values_list("email", flat=True)

    if superusers_emails:
        # Send Email asynchronously
        EmailThread(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=superusers_emails,
            is_admin_alert=True,
        ).start()
