# Generated by Django 4.1.1 on 2022-12-09 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_group_remove_user_name_notes_group_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='file_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]