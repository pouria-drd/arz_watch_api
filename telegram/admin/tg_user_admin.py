from datetime import timedelta
from django.contrib import admin
from django.utils import timezone
from django.http import JsonResponse
from telegram.models import TelegramUser
from django.contrib.admin import SimpleListFilter


class OnlineFilter(SimpleListFilter):
    title = "online status"
    parameter_name = "online"

    def lookups(self, request, model_admin):
        return (
            ("online", "Online (seen last 5 min)"),
            ("offline", "Offline"),
        )

    def queryset(self, request, queryset):
        if self.value() == "online":
            return queryset.filter(
                last_seen__gte=timezone.now() - timezone.timedelta(minutes=5)
            )
        if self.value() == "offline":
            return queryset.filter(
                last_seen__lt=timezone.now() - timezone.timedelta(minutes=5)
            )


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
        "username",
        "full_name",
        "phone_number",
        "is_bot",
        "is_premium",
        "status",
        "is_online_display",
        "language_code",
        "last_seen",
        "created_at",
    ]

    list_filter = [
        "is_bot",
        "is_premium",
        "status",
        "language_code",
        OnlineFilter,
    ]

    search_fields = [
        "user_id",
        "username",
        "first_name",
        "last_name",
        "phone_number",
    ]

    readonly_fields = [
        "created_at",
        "last_seen",
        "user_id",
    ]

    date_hierarchy = "last_seen"

    actions = [
        "ban_users",
        "activate_users",
        "export_as_json",
    ]

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "user_id",
                    "username",
                    "first_name",
                    "last_name",
                    "phone_number",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "is_active",
                    "is_bot",
                    "is_premium",
                    "language_code",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "last_seen",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def is_online_display(self, obj):
        return obj.is_online()

    is_online_display.boolean = True
    is_online_display.short_description = "Online"

    def ban_users(self, request, queryset):
        queryset.update(status="banned", is_active=False)
        self.message_user(request, f"{queryset.count()} users banned")

    ban_users.short_description = "Ban selected users"

    def activate_users(self, request, queryset):
        queryset.update(status="active", is_active=True)
        self.message_user(request, f"{queryset.count()} users activated")

    activate_users.short_description = "Activate selected users"

    def export_as_json(self, request, queryset):
        data = list(
            queryset.values(
                "user_id",
                "username",
                "first_name",
                "last_name",
                "phone_number",
                "is_bot",
                "is_premium",
                "language_code",
                "status",
                "last_seen",
            )
        )
        return JsonResponse(data, safe=False)

    export_as_json.short_description = "Export as JSON"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["stats"] = {
            "total": TelegramUser.objects.count(),
            "active": TelegramUser.objects.filter(is_active=True).count(),
            "bots": TelegramUser.objects.filter(is_bot=True).count(),
            "online": TelegramUser.objects.filter(
                last_seen__gte=timezone.now() - timedelta(minutes=5)
            ).count(),
        }
        return super().changelist_view(request, extra_context=extra_context)
