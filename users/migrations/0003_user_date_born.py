# Generated by Django 5.1.2 on 2024-11-05 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="date_born",
            field=models.DateField(blank=True, null=True, verbose_name="Дата рождения"),
        ),
    ]