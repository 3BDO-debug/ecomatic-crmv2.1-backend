# Generated by Django 3.2.5 on 2021-08-08 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tickets', '0010_auto_20210808_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='gasoveninstallationrequirementsform',
            name='gas_pressure',
            field=models.CharField(default='21', max_length=350, verbose_name='Gas Pressure'),
            preserve_default=False,
        ),
    ]