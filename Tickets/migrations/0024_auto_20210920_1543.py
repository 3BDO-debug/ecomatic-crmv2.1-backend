# Generated by Django 3.2.5 on 2021-09-20 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tickets', '0023_auto_20210917_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketfollowbackcallrating',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='ticketfollowbackcallrating',
            name='rating',
        ),
        migrations.AddField(
            model_name='ticketfollowbackcallrating',
            name='agent_stage_rating',
            field=models.IntegerField(blank=True, null=True, verbose_name='Agent stage rating'),
        ),
        migrations.AddField(
            model_name='ticketfollowbackcallrating',
            name='follow_up_notes',
            field=models.TextField(blank=True, null=True, verbose_name='Follow up notes'),
        ),
        migrations.AddField(
            model_name='ticketfollowbackcallrating',
            name='overall_rating',
            field=models.IntegerField(blank=True, null=True, verbose_name='Overall rating'),
        ),
        migrations.AddField(
            model_name='ticketfollowbackcallrating',
            name='technicial_support_stage_rating',
            field=models.IntegerField(blank=True, null=True, verbose_name='Technicial support stage rating'),
        ),
        migrations.AddField(
            model_name='ticketfollowbackcallrating',
            name='technician_rating',
            field=models.IntegerField(blank=True, null=True, verbose_name='Technician rating'),
        ),
        migrations.CreateModel(
            name='TicketFollowbackCallDeviceRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, null=True, verbose_name='Rating')),
                ('related_ticket_device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tickets.ticketdevice', verbose_name='Related ticket device')),
                ('related_ticket_follow_back_call', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tickets.ticketfollowbackcallrating', verbose_name='Related ticket follow back call device rating')),
            ],
        ),
    ]
