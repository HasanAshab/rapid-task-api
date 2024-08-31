# Generated by Django 5.0 on 2024-05-08 04:10

import datetime_validators.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("difficulties", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Challenge",
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
                    "title",
                    models.CharField(
                        help_text="Title of the challenge.",
                        max_length=50,
                        verbose_name="Title",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Description of the challenge.",
                        max_length=200,
                        verbose_name="Description",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="active",
                        help_text="Status of the challenge.",
                        max_length=10,
                        verbose_name="Status",
                    ),
                ),
                (
                    "is_pinned",
                    models.BooleanField(
                        default=False,
                        help_text="Whether the challenge is pinned.",
                        verbose_name="Is Pinned",
                    ),
                ),
                (
                    "due_date",
                    models.DateTimeField(
                        help_text="Due date of the challenge.",
                        null=True,
                        validators=[
                            datetime_validators.validators.date_time_is_future_validator
                        ],
                        verbose_name="Due Date",
                    ),
                ),
                (
                    "order",
                    models.IntegerField(
                        default=1,
                        help_text="Priority order of the challenge.",
                        verbose_name="Order",
                    ),
                ),
                (
                    "difficulty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="difficulties.difficulty",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
