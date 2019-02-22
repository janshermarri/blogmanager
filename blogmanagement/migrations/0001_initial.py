# Generated by Django 2.1.6 on 2019-02-11 12:10

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('contact', models.CharField(max_length=200)),
                ('date_joined', models.DateTimeField(default=datetime.datetime(2019, 2, 11, 12, 10, 46, 3680, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=400)),
                ('post_body', models.TextField()),
                ('keywords', models.TextField()),
                ('date_created', models.DateTimeField(default=datetime.datetime(2019, 2, 11, 12, 10, 46, 14739, tzinfo=utc))),
                ('date_published', models.DateTimeField(default=None)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogmanagement.Author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogmanagement.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogmanagement.Status'),
        ),
    ]
