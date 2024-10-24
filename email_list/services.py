import smtplib
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.mail import send_mail

from email_list.models import MailingSettings, Attempt
from apscheduler.schedulers.background import BackgroundScheduler


def send_newsletter_email(mailing_settings):
    try:
        server_response = send_mail(
            subject=mailing_settings.mail_message.subject,
            message=mailing_settings.mail_message.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing_settings.clients.all()],
            fail_silently=False,
        )
        log = Attempt.objects.filter(mailing_settings=mailing_settings)[0]
        zone = pytz.timezone(settings.TIME_ZONE)
        log.last_attempt_datetime = datetime.now(zone)

        if server_response:
            log.status = "Успешно"
            log.save()
        if (
            mailing_settings.status == "создана"
            or mailing_settings.status == "завершена"
        ):
            mailing_settings.status = "запущена"
            mailing_settings.save()
    except smtplib.SMTPException as e:
        log = Attempt.objects.filter(mailing_settings=mailing_settings)[0]
        zone = pytz.timezone(settings.TIME_ZONE)
        log.last_attempt_datetime = datetime.now(zone)
        log.server_response = e
        log.status = "Не успешно"
        log.save()
        mailing_settings.status = "запущена"
        mailing_settings.save()
    print(f"Попытка рассылки: {log.status}")


def send_newsletter_periodic_email():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    print(f"Текущее время - {current_datetime}")

    for obj in MailingSettings.objects.filter(is_active=True):
        if Attempt.objects.filter(mailing_settings=obj).exists():
            log = Attempt.objects.filter(mailing_settings=obj)[0]
        else:
            log = Attempt.objects.create(
                mailing_settings=obj, last_attempt_datetime=current_datetime
            )
            print("Первая попытка рассылки")
            send_newsletter_email(obj)

        if obj.start_datetime < current_datetime < obj.end_datetime:

            current_timedelta = current_datetime - log.last_attempt_datetime

            if obj.period == "per_day" and current_timedelta >= timedelta(days=1):
                send_newsletter_email(obj)
                print(f"Выполнена повторная рассылка раз в день")
            elif obj.period == "per_week" and current_timedelta >= timedelta(weeks=1):
                send_newsletter_email(obj)
                print(f"Выполнена повторная рассылка раз в неделю")
            elif obj.period == "per_month" and current_timedelta >= timedelta(weeks=4):
                send_newsletter_email(obj)
                print(f"Выполнена повторная рассылка раз в месяц")

        elif current_datetime > obj.end_datetime:
            obj.status = "завершена"
            obj.is_active = False
            obj.save()


def start_scheduler():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    if not scheduler.get_jobs():
        print("Создание работы")
        scheduler.add_job(send_newsletter_periodic_email, "interval", seconds=60)

    if not scheduler.running:
        print("Запуск планировщика")
        scheduler.start()
