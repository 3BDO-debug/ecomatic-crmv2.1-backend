# Generated by Django 3.2.5 on 2021-09-03 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tickets', '0015_alter_ticketdevice_extra_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='ticket_generated_id',
            field=models.CharField(default='dasd', max_length=350, verbose_name='Ticket ID'),
            preserve_default=False,
        ),
    ]
