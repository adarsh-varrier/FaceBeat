# Generated by Django 5.1.1 on 2024-10-28 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0013_remove_music_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='genre',
            field=models.CharField(blank=True, default='null', max_length=100),
        ),
    ]
