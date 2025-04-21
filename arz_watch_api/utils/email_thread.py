import threading
from logging import getLogger
from django.utils import timezone
from django.core.mail import send_mail

# Initialize logger for email notifications
logger = getLogger("email_v1")


class EmailThread(threading.Thread):
    """Thread for sending emails asynchronously."""

    def __init__(
        self,
        subject: str,
        message: str,
        from_email: str,
        recipient_list: list,
        fail_silently=False,
        is_admin_alert=False,
    ):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.fail_silently = fail_silently
        self.is_admin_alert = is_admin_alert
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(
                subject=self.subject,
                message=self.message,
                from_email=self.from_email,
                recipient_list=self.recipient_list,
                fail_silently=self.fail_silently,
            )
            if self.is_admin_alert:
                logger.info(
                    f"Info:Async email sent | Detail:subject={self.subject} | Date:{timezone.now()}"
                )
            else:
                logger.info(
                    f"Info:Async email sent | Detail:subject={self.subject}, emails={self.recipient_list} | Date:{timezone.now()}"
                )

        except Exception as e:
            logger.error(
                f"Error:Failed to send async email | Detail:subject={self.subject}, error={str(e)} | Date:{timezone.now()}"
            )
