# Generated by Django 2.2.5 on 2019-09-25 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roulette', '0002_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]