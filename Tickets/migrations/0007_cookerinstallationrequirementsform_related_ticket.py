# Generated by Django 3.2.5 on 2021-08-07 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tickets', '0006_hoodinstallationrequirementsform_related_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookerinstallationrequirementsform',
            name='related_ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tickets.ticket'),
        ),
    ]
