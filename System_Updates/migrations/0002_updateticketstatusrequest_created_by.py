# Generated by Django 3.2.5 on 2021-07-11 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System_Updates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='updateticketstatusrequest',
            name='created_by',
            field=models.CharField(default='Employee Full Name Goes Here', max_length=350, verbose_name='Created By'),
            preserve_default=False,
        ),
    ]
