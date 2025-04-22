import uuid
from django.db import models
from django.utils import timezone


class TelegramUser(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("banned", "Banned"),
        ("inactive", "Inactive"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)

    is_bot = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    language_code = models.CharField(max_length=10, blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["username"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["last_seen"]),
        ]
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"

    def __str__(self):
        name = self.username or f"{self.first_name} {self.last_name}".strip()
        return f"{name} ({self.user_id})"

    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    def is_online(self):
        return (timezone.now() - self.last_seen) < timezone.timedelta(minutes=5)

    def update_last_seen(self):
        self.last_seen = timezone.now()
        self.save(update_fields=["last_seen"])
