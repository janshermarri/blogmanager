# Generated by Django 2.1.6 on 2019-02-14 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogmanagement', '0005_quotes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('author', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Quotes',
        ),
    ]
