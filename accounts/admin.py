from django.contrib import admin
from .models import SupportTicket
from django.contrib import admin
from .models import SupportTicket
from .models import BugReport
@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "subject",
        "short_message",
        "created_at",
        "is_resolved",
    )

    list_filter = (
        "is_resolved",
        "created_at",
    )

    search_fields = (
        "user__username",
        "subject",
        "message",
    )

    list_editable = (
        "is_resolved",
    )

    ordering = (
        "-created_at",
    )

    def short_message(self, obj):

        if len(obj.message) > 50:

            return obj.message[:50] + "..."

        return obj.message

    short_message.short_description = "Message"

@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "title",
        "page",
        "created_at",
        "is_fixed",
    )

    list_filter = (
        "is_fixed",
        "created_at",
    )

    search_fields = (
        "user__username",
        "title",
        "description",
    )

    list_editable = (
        "is_fixed",
    )

    ordering = (
        "-created_at",
    )