# Generated by Django 2.2.5 on 2019-09-25 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roulette', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_name', to='roulette.Restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='roulette.User')),
            ],
        ),
    ]