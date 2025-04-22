import uuid
import secrets
from django.db import models
from django.utils import timezone


class APIKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True, editable=False)

    request_count = models.PositiveIntegerField(default=0)
    max_requests = models.PositiveIntegerField(default=1000)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_request_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"
        indexes = [
            models.Index(fields=["key"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.name} ({status}, {self.request_count}/{self.max_requests})"

    def is_valid(self):
        if not self.is_active or self.is_deleted:
            return False

        if self.request_count >= self.max_requests:
            return False

        if self.expires_at and timezone.now() > self.expires_at:
            self.is_active = False
            self.save()
            return False

        return True

    def increment_usage(self):
        self.request_count += 1
        self.last_request_at = timezone.now()
        self.save()

    def reset_usage(self):
        self.request_count = 0
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def regenerate_key(self):
        self.key = self.generate_key()
        self.save()

    @classmethod
    def generate_key(cls):
        return secrets.token_hex(32)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)
