from django.contrib import admin
from telegram.models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "username",
        "first_name",
        "last_name",
        "is_bot",
        "is_premium",
        "language_code",
        "is_active",
        "last_seen",
        "created_at",
    )
    list_filter = ("is_bot", "is_premium", "language_code", "is_active")
    search_fields = ("user_id", "username", "first_name", "last_name")
    readonly_fields = ("created_at", "last_seen")
    ordering = ("-last_seen",)
