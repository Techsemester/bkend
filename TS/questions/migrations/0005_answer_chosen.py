# Generated by Django 3.0.6 on 2021-06-18 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20210618_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='chosen',
            field=models.BooleanField(default=False),
        ),
    ]
