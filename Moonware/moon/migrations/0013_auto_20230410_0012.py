# Generated by Django 3.2 on 2023-04-09 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moon', '0012_report_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='firstImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='static/postImgs')),
            ],
        ),
        migrations.CreateModel(
            name='pdf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(blank=True, null=True, upload_to='static/files')),
            ],
        ),
        migrations.CreateModel(
            name='secondImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='static/postImgs')),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='fistImage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moon.firstimg'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pdf',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moon.pdf'),
        ),
        migrations.AlterField(
            model_name='post',
            name='secondImage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moon.secondimg'),
        ),
    ]
