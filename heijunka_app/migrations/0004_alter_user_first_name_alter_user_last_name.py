# Generated by Django 5.1.1 on 2024-10-10 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heijunka_app', '0003_remove_user_full_name_user_first_name_user_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='null', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='null', max_length=50),
        ),
    ]