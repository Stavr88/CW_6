from django.contrib import admin

from email_list.models import Client, MailingMessage, MailingSettings, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "patronymic",
        "email",
    )
    search_fields = (
        "first_name",
        "last_name",
        "patronymic",
        "email",
    )


@admin.register(MailingMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "message",
    )
    search_fields = (
        "subject",
        "message",
    )


@admin.register(MailingSettings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "period",
        "start_datetime",
        "end_datetime",
        "is_active",
    )
    list_filter = (
        "is_active",
        "period",
        "start_datetime",
        "end_datetime",
    )


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "last_attempt_datetime",
    )
    list_filter = (
        "status",
        "last_attempt_datetime",
    )
