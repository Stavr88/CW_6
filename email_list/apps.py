import os

from django.apps import AppConfig


class EmailListConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "email_list"

    def ready(self):
        if os.environ.get("RUN_MAIN"):
            from email_list.services import start_scheduler

            start_scheduler()
