# Generated by Django 3.2.5 on 2021-08-11 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tickets', '0012_ticketdevice_customer_service_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketdevice',
            name='re_opened',
            field=models.BooleanField(blank=True, null=True, verbose_name='Re Opened'),
        ),
    ]