# Generated by Django 4.0.4 on 2022-05-29 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strolchguru', '0006_clip_category_clip_is_in_loop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clip',
            name='tags',
            field=models.ManyToManyField(blank=True, to='strolchguru.tag'),
        ),
    ]
