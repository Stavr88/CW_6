from django.core.management import BaseCommand
from django_apscheduler.models import DjangoJobExecution

from email_list.services import start_scheduler


class Command(BaseCommand):
    """
    Команда на запуск рассылки
    Запускается командой - manage.py mail каждый раз, когда запускается веб-сервер, обслуживающий ваше приложение Django
    """

    def handle(self, *args, **options):
        start_scheduler()


def delete_old_job_executions(max_age=604_800):
    """
   Этот метод удаляет из базы данных записи выполнения заданий APScheduler старше max_age.
   Это помогает предотвратить заполнение базы данных старыми историческими записями,
   которые больше не нужны.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
