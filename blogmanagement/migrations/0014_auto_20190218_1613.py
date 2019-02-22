# Generated by Django 2.1.6 on 2019-02-18 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogmanagement', '0013_auto_20190218_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='slug',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=47, on_delete=django.db.models.deletion.CASCADE, to='blogmanagement.Author'),
        ),
    ]