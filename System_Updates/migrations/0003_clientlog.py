# Generated by Django 3.2.5 on 2021-09-14 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Clients', '0015_clientdevice_created_at'),
        ('System_Updates', '0002_missingdatarequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=350, verbose_name='Action done')),
                ('created_by', models.CharField(max_length=350, verbose_name='Created by')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('related_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Clients.client', verbose_name='Related client')),
            ],
            options={
                'verbose_name': 'Client log',
                'verbose_name_plural': 'Client logs',
            },
        ),
    ]