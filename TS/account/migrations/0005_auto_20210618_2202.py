# Generated by Django 3.0.6 on 2021-06-18 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210609_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='total_answers',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='total_questions',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ts_rank',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
