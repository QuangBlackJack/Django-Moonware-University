# Generated by Django 3.2 on 2023-03-23 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moon', '0003_alter_userinfo_gif'),
    ]

    operations = [
        migrations.CreateModel(
            name='season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('firstDeadline', models.DateField()),
                ('secondDeadline', models.DateField()),
            ],
        ),
    ]
