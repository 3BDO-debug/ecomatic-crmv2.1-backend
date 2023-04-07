# Generated by Django 3.2.5 on 2021-09-17 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tickets', '0022_ticket_ticket_forced_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookerinstallationrequirementsform',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='Cooker_Installation_Attachment', verbose_name='Attachment'),
        ),
        migrations.AddField(
            model_name='electricoveninstallationrequirementsform',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='Electric_Oven_Installation_Attachment', verbose_name='Attachment'),
        ),
        migrations.AddField(
            model_name='gasoveninstallationrequirementsform',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='Gas_Oven_Installation_Attachment', verbose_name='Attachment'),
        ),
        migrations.AddField(
            model_name='hoodinstallationrequirementsform',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='Hood_Installation_Attachment', verbose_name='Attachment'),
        ),
        migrations.AddField(
            model_name='slimhobinstallationrequirementsform',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='Slim_Hob_Installation_Attachment', verbose_name='Attachment'),
        ),
        migrations.AddField(
            model_name='ticketdevice',
            name='not_completed_attachment',
            field=models.FileField(blank=True, null=True, upload_to='Not_Completed_Attachment', verbose_name='Not completed attachment'),
        ),
    ]