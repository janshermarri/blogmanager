# Generated by Django 2.1.6 on 2019-02-14 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogmanagement', '0007_auto_20190214_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='author',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]