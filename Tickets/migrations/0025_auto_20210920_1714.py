# Generated by Django 3.2.5 on 2021-09-20 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tickets', '0024_auto_20210920_1543'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TicketFollowbackCallDeviceRating',
            new_name='TicketFollowUpCallDeviceRating',
        ),
        migrations.RenameModel(
            old_name='TicketFollowbackCallRating',
            new_name='TicketFollowUpCallRating',
        ),
        migrations.AlterModelOptions(
            name='ticketfollowupcallrating',
            options={'verbose_name': 'Ticket Follow Up Call Rating', 'verbose_name_plural': 'Ticket Follow Up Call Ratings'},
        ),
    ]
