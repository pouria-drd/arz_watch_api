import csv
from datetime import timedelta
from django.contrib import admin
from api_keys.models import APIKey
from django.http import HttpResponse
from django.utils.timezone import now
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter


class ExpiredFilter(SimpleListFilter):
    title = "expiration status"
    parameter_name = "expired"

    def lookups(self, request, model_admin):
        return (
            ("expired", "Expired"),
            ("active", "Active"),
            ("expiring_soon", "Expiring soon (7 days)"),
        )

    def queryset(self, request, queryset):
        now_ = now()
        if self.value() == "expired":
            return queryset.filter(expires_at__lt=now_)
        if self.value() == "active":
            return queryset.filter(expires_at__gte=now_) | queryset.filter(
                expires_at__isnull=True
            )
        if self.value() == "expiring_soon":
            return queryset.filter(
                expires_at__gte=now_, expires_at__lte=now_ + timedelta(days=7)
            )


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "masked_key",
        "request_count",
        "max_requests",
        "usage_percentage",
        "is_active",
        "created_at",
        "expires_at",
        "last_request_at",
        "expiration_status",
    )

    list_filter = ("is_active", "created_at", ExpiredFilter)
    search_fields = ("name", "key")
    date_hierarchy = "created_at"
    # list_editable = ("max_requests", "is_active")
    readonly_fields = ("key", "created_at", "updated_at")
    actions = [
        "reset_request_count",
        "activate_keys",
        "deactivate_keys",
        "extend_expiration",
        "export_as_csv",
    ]

    fieldsets = (
        ("Basic Info", {"fields": ("name", "key", "is_active")}),
        (
            "Usage Limits",
            {
                "fields": ("request_count", "max_requests", "expires_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def masked_key(self, obj):
        return f"{obj.key[:4]}...{obj.key[-4:]}" if len(obj.key) > 8 else obj.key

    masked_key.short_description = "API Key"

    def usage_percentage(self, obj):
        return f"{min(100, int((obj.request_count / obj.max_requests) * 100))}%"

    usage_percentage.short_description = "Usage"

    def expiration_status(self, obj):
        if not obj.is_active:
            return format_html('<span style="color:gray;">Inactive</span>')
        if obj.expires_at:
            if obj.expires_at < now():
                return format_html('<span style="color:red;">Expired</span>')
            if (obj.expires_at - now()).days < 7:
                return format_html('<span style="color:orange;">Expires soon</span>')
        return format_html('<span style="color:green;">Active</span>')

    expiration_status.short_description = "Status"

    def reset_request_count(self, request, queryset):
        updated = queryset.update(request_count=0)
        self.message_user(
            request, f"Reset count for {updated} key{'s' if updated != 1 else ''}."
        )

    def activate_keys(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request, f"Activated {updated} key{'s' if updated != 1 else ''}."
        )

    def deactivate_keys(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request, f"Deactivated {updated} key{'s' if updated != 1 else ''}."
        )

    def extend_expiration(self, request, queryset):
        for obj in queryset:
            if obj.expires_at:
                obj.expires_at += timedelta(days=30)
                obj.save()
        self.message_user(request, "Extended expiration by 30 days.")

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="api_keys.csv"'

        writer = csv.writer(response)
        writer.writerow(["Name", "Key", "Requests", "Max", "Status"])
        for obj in queryset:
            writer.writerow(
                [
                    obj.name,
                    obj.key,
                    obj.request_count,
                    obj.max_requests,
                    "Active" if obj.is_active else "Inactive",
                ]
            )
        return response
