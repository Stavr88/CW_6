# Generated by Django 4.2.2 on 2024-07-09 17:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Почта"
                    ),
                ),
                ("first_name", models.CharField(max_length=20, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=30, verbose_name="Фамилия")),
                (
                    "patronymic",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Отчество"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Комментарий"),
                ),
            ],
            options={
                "verbose_name": "клиент",
                "verbose_name_plural": "клиенты",
            },
        ),
        migrations.CreateModel(
            name="MailingMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subject",
                    models.CharField(max_length=100, verbose_name="Тема письма"),
                ),
                (
                    "message",
                    models.TextField(blank=True, null=True, verbose_name="Сообщение"),
                ),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
            },
        ),
        migrations.CreateModel(
            name="MailingSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_datetime",
                    models.DateTimeField(
                        default=datetime.datetime.now, verbose_name="Начало рассылки"
                    ),
                ),
                (
                    "end_datetime",
                    models.DateTimeField(
                        default=datetime.datetime.now, verbose_name="Окончание рассылки"
                    ),
                ),
                (
                    "period",
                    models.CharField(
                        choices=[
                            ("per_day", "раз в день"),
                            ("per_week", "раз в неделю"),
                            ("per_month", "раз в месяц"),
                        ],
                        default="per_month",
                        max_length=15,
                        verbose_name="Период рассылки",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "создана"),
                            ("started", "запущена"),
                            ("completed", "завершена"),
                        ],
                        default="created",
                        max_length=15,
                        verbose_name="Статус рассылки",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="Активна"),
                ),
                (
                    "clients",
                    models.ManyToManyField(
                        to="email_list.client", verbose_name="Получатели"
                    ),
                ),
                (
                    "mail_message",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="email_list.mailingmessage",
                        verbose_name="Сообщение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
        migrations.CreateModel(
            name="Attempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_attempt_datetime",
                    models.DateTimeField(
                        auto_now=True,
                        null=True,
                        verbose_name="Дата и время последней попытки рассылки",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[(True, "Успешно"), (False, "Не успешно")],
                        default=True,
                        max_length=10,
                        null=True,
                        verbose_name="Статус попытки",
                    ),
                ),
                (
                    "mailing_settings",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="email_list.mailingsettings",
                        verbose_name="Рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Попытка рассылки",
                "verbose_name_plural": "Попытки рассылки",
            },
        ),
    ]