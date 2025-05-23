from datetime import timedelta
from django.contrib import admin
from django.utils import timezone
from django.http import JsonResponse
from telegram.models import TelegramUser
from django.utils.html import format_html
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
        "status",
        "request_count",
        "max_requests",
        "usage_percentage",
        "is_bot",
        "is_premium",
        "is_online_display",
        "can_make_request_display",
        "language_code",
        "last_seen",
        "created_at",
        "last_reset_at",
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
    ]

    readonly_fields = [
        "created_at",
        "last_seen",
        "user_id",
    ]

    date_hierarchy = "last_seen"

    actions = [
        "reset_request_count",
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
            "Requests",
            {
                "fields": (
                    "request_count",
                    "max_requests",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "last_seen",
                    "last_reset_at",
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

    def reset_request_count(self, request, queryset):
        queryset.update(request_count=0)
        self.message_user(request, f"{queryset.count()} users' request count reset")

    reset_request_count.short_description = "Reset request count"

    def can_make_request_display(self, obj):
        return obj.can_make_request()

    can_make_request_display.boolean = True
    can_make_request_display.short_description = "Can make request"

    def usage_percentage(self, obj):
        """
        Calculates the usage percentage of requests.
        """
        if obj.max_requests > 0:
            percent = (obj.request_count / obj.max_requests) * 100
            return format_html("<b>{:.2}%</b>", float(percent))
        else:
            return "N/A"

    usage_percentage.short_description = "Usage (%)"
