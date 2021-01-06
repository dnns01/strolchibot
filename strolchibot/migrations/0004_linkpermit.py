# Generated by Django 3.1.2 on 2021-01-06 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strolchibot', '0003_config'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkPermit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick', models.CharField(max_length=25)),
            ],
        ),
        migrations.RunSQL(
            "INSERT INTO strolchibot_config VALUES('LinkProtectionActive', '0')"
        ),
        migrations.RunSQL(
            "INSERT INTO strolchibot_config VALUES('LinkProtectionPermitSubs', '0')"
        )
    ]