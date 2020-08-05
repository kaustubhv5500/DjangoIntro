# Generated by Django 3.0.2 on 2020-03-24 07:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_auto_20200322_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, help_text='Category of Website', max_length=31, unique=True),
            preserve_default=False,
        ),
    ]
