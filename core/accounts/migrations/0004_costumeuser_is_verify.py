# Generated by Django 5.0.7 on 2024-08-02 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_profilemodel_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="costumeuser",
            name="is_verify",
            field=models.BooleanField(default=False),
        ),
    ]
