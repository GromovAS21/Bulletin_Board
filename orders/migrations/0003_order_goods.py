# Generated by Django 5.1.2 on 2024-11-04 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("announcements", "0001_initial"),
        ("orders", "0002_alter_order_amount_alter_order_author_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="goods",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                to="announcements.announcement",
                verbose_name="Товары",
            ),
        ),
    ]
