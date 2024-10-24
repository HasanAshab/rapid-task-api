# Generated by Django 5.0 on 2024-10-16 05:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("difficulties", "0002_difficulty_score"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="difficulty",
            options={"ordering": ("score",)},
        ),
        migrations.AlterField(
            model_name="difficulty",
            name="score",
            field=models.FloatField(
                help_text="The score of the difficulty level.",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(1000),
                ],
                verbose_name="Score",
            ),
        ),
    ]
