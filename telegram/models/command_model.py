import uuid
from django.db import models
from .tg_user_models import TelegramUser


class TelegramCommand(models.Model):
    COMMAND_TYPES = [
        ("coin", "Coin"),
        ("gold", "Gold"),
        ("crypto", "Crypto"),
        ("currency", "Currency"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    tg_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.SET_NULL,
        related_name="commands",
        null=True,
        blank=True,
        db_index=True,
    )

    command_type = models.CharField(
        max_length=10,
        choices=COMMAND_TYPES,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Telegram Command"
        verbose_name_plural = "Telegram Commands"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["tg_user"]),
            models.Index(fields=["command_type"]),
            models.Index(fields=["created_at"]),
        ]
