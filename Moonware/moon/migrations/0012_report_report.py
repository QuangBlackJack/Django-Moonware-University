# Generated by Django 3.2 on 2023-04-05 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moon', '0011_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='report',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
