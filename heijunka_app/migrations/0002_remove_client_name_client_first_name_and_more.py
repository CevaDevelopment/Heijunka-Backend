# Generated by Django 5.1.1 on 2024-10-17 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heijunka_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='name',
        ),
        migrations.AddField(
            model_name='client',
            name='first_name',
            field=models.CharField(default='Desconocido', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='last_name',
            field=models.CharField(default='Desconocido', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'Admin'), ('manager', 'Manager'), ('operator', 'operator')], default='operator', max_length=10, null=True),
        ),
    ]
