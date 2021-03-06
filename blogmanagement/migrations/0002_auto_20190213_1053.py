# Generated by Django 2.1.6 on 2019-02-13 05:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='slug',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
