# Generated by Django 4.1.1 on 2022-10-05 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BasePlayer",
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
                ("name", models.CharField(max_length=100)),
                ("date_of_birth", models.DateField()),
                ("nationality", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="League",
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
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=10)),
                ("area", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Coach",
            fields=[
                (
                    "baseplayer_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="be_challenge_app.baseplayer",
                    ),
                ),
            ],
            bases=("be_challenge_app.baseplayer",),
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "baseplayer_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="be_challenge_app.baseplayer",
                    ),
                ),
                ("position", models.CharField(max_length=100)),
            ],
            bases=("be_challenge_app.baseplayer",),
        ),
        migrations.CreateModel(
            name="Team",
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
                ("name", models.CharField(max_length=100)),
                ("short_name", models.CharField(max_length=10)),
                ("area", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=100)),
                ("league", models.ManyToManyField(to="be_challenge_app.league")),
            ],
        ),
        migrations.AddField(
            model_name="baseplayer",
            name="team",
            field=models.ManyToManyField(to="be_challenge_app.team"),
        ),
    ]
