# Generated by Django 3.2.5 on 2021-07-15 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clients', '0011_alter_clientdevice_expected_warranty_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdevice',
            name='installed_through_the_company',
            field=models.BooleanField(blank=True, null=True, verbose_name='Installed Through The Company'),
        ),
    ]
