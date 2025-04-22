from django.contrib import admin
from telegram.models import TelegramCommand


@admin.register(TelegramCommand)
class TelegramCommandAdmin(admin.ModelAdmin):
    list_display = (
        "tg_user",
        "command_type",
        "created_at",
    )
    list_filter = ("command_type",)
    search_fields = ("tg_user__user_id", "tg_user__username", "tg_user__first_name")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
