# Generated by Django 4.1.1 on 2023-02-14 22:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_audio_date_audio_file_text_audio_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
