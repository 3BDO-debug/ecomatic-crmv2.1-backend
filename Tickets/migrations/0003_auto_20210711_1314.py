# Generated by Django 3.2.5 on 2021-07-11 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Storage', '0001_initial'),
        ('Tickets', '0002_auto_20210711_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketdevicespareparts',
            name='assigned_spareparts',
        ),
        migrations.AddField(
            model_name='ticketdevicespareparts',
            name='assigned_sparepart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Storage.sparepart', verbose_name='Assigned Spareparts'),
        ),
        migrations.AddField(
            model_name='ticketdevicespareparts',
            name='required_qty',
            field=models.IntegerField(default=1, verbose_name='Required QTY'),
            preserve_default=False,
        ),
    ]
