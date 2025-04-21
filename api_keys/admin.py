from django.contrib import admin
from api_keys.models import APIKey
from django.utils.timezone import now
from django.utils.html import format_html


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    # Correctly define list_display as a tuple
    list_display = (
        "name",
        "key",
        "request_count",
        "is_active",
        "created_at",
        "expires_at",
        "is_expired",
    )

    # Add filters for quick searching
    list_filter = ("is_active", "created_at", "expires_at")

    # Add search functionality by 'name' and 'key'
    search_fields = ("name", "key")

    # Allow date range filtering
    date_hierarchy = "created_at"

    # Allow for bulk actions (enable deactivating multiple keys)
    actions = ["activate_keys", "deactivate_keys"]

    # Helper method to display if the API key is expired
    def is_expired(self, obj):
        if obj.expires_at and obj.expires_at < now():
            return format_html('<span style="color:red;">Expired</span>')
        return format_html('<span style="color:green;">Active</span>')

    is_expired.short_description = "Expiration Status"

    def activate_keys(self, request, queryset):
        rows_updated = queryset.update(is_active=True)
        if rows_updated == 1:
            message_bit = "1 key was"
        else:
            message_bit = f"{rows_updated} keys were"
        self.message_user(request, f"{message_bit} successfully activated.")

    # Custom bulk action to deactivate selected keys
    def deactivate_keys(self, request, queryset):
        rows_updated = queryset.update(is_active=False)
        if rows_updated == 1:
            message_bit = "1 key was"
        else:
            message_bit = f"{rows_updated} keys were"
        self.message_user(request, f"{message_bit} successfully deactivated.")

    deactivate_keys.short_description = "Deactivate selected keys"

    # Use readonly_fields for 'created_at' and prevent editing
    readonly_fields = ("key", "created_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "key",
                    "is_active",
                    "expires_at",
                )
            },
        ),
    )
