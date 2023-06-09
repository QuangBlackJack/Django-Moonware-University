# Generated by Django 3.2 on 2023-03-21 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=b'I00\n', null=b'I00\n', upload_to='static/avatars')),
            ],
        ),
        migrations.CreateModel(
            name='gif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gifLink', models.URLField(default='', max_length=255)),
            ],
        ),
    ]
