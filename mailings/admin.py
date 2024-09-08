from django.contrib import admin

from mailings.models import Message, EmailClient, Mailings


# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "message_title", "message_text")
    list_filter = ("message_title",)
    search_fields = (
        "message_title",
        "message_text",
    )


@admin.register(EmailClient)
class EmailClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "comment")
    list_filter = ("name", "email",)
    search_fields = (
        "name",
        "email",
    )


@admin.register(Mailings)
class MailingsAdmin(admin.ModelAdmin):
    list_display = ("id", "launch_at", "completed_at", "periodicity", "status", "message", "get_email_client")
    list_filter = ("launch_at", "completed_at", "periodicity", "status", "message")
    search_fields = (
        "launch_at",
        "completed_at",
        "periodicity",
        "status",
    )
