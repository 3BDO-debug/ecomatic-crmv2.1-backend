# Generated by Django 3.2.5 on 2021-10-02 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tickets', '0026_ticket_related_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketdevice',
            name='agent_attachment',
            field=models.FileField(blank=True, null=True, upload_to='agent_attachments', verbose_name='Agent attachments'),
        ),
    ]
