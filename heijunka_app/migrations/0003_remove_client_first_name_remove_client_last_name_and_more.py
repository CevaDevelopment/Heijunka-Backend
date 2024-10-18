# Generated by Django 5.1.1 on 2024-10-17 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heijunka_app', '0002_remove_client_name_client_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='last_name',
        ),
        migrations.AddField(
            model_name='client',
            name='name',
            field=models.CharField(default='Cliente', max_length=100),
            preserve_default=False,
        ),
    ]