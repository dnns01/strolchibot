# Generated by Django 3.2.8 on 2021-12-20 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strolchibot', '0009_spotify'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='config',
            name='key',
        ),
        migrations.RemoveField(
            model_name='config',
            name='value',
        ),
        migrations.AddField(
            model_name='config',
            name='link_protection_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='config',
            name='link_protection_permit_subs',
            field=models.BooleanField(default=True),
        ),
    ]
