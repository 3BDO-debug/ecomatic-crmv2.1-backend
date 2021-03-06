# Generated by Django 3.2.5 on 2021-08-07 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tickets', '0003_alter_ticket_total_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='CookerInstallationRequirementsForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cooker_model_number', models.CharField(max_length=350, verbose_name='Cooker Model Number')),
                ('gas_type', models.CharField(max_length=350, verbose_name='Gas Type')),
                ('gas_pressure', models.CharField(max_length=350, verbose_name='Gas Pressure')),
                ('stabilizer_type', models.CharField(max_length=350, verbose_name='Stabilizer Type')),
                ('cooker_fonia_number', models.CharField(max_length=350, verbose_name='Cooker Fonia Number')),
                ('grill_fonia_number', models.CharField(max_length=350, verbose_name='Grill Fonia Number')),
                ('whats_done_by_the_technician', models.TextField(verbose_name="What's Done By The Technician")),
                ('cooker_final_condition', models.TextField(verbose_name='Cooker Final Condition')),
                ('client_signature', models.CharField(max_length=350, verbose_name='Client Signature')),
                ('technician_name', models.CharField(max_length=350, verbose_name='Technician Name')),
                ('notes', models.TextField(verbose_name='Notes')),
            ],
        ),
        migrations.CreateModel(
            name='ElectricOvenInstallationRequirementsForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('electric_oven_model_number', models.CharField(max_length=350, verbose_name='Electricc Oven Model Number')),
                ('ventillation_hole_is_available', models.BooleanField(default=True, verbose_name='Ventillation Hole Is Available')),
                ('ventillation_hole_measurements', models.CharField(max_length=350, verbose_name='Ventillation Hole Measurements')),
                ('notes', models.TextField(verbose_name='Notes')),
                ('whats_done_by_the_technician', models.TextField(verbose_name="What's Done By The Technician")),
                ('electric_oven_final_condition', models.TextField(verbose_name='Electric Oven Final Condition')),
                ('client_signature', models.CharField(max_length=350, verbose_name='Client Signature')),
                ('technician_name', models.CharField(max_length=350, verbose_name='Technician Name')),
            ],
        ),
        migrations.CreateModel(
            name='GasOvenInstallationRequirementsForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gas_oven_model_number', models.CharField(max_length=350, verbose_name='Gas Oven Model Number')),
                ('gas_type', models.CharField(max_length=350, verbose_name='Gas Type')),
                ('ventillation_hole_below_oven_is_available', models.BooleanField(default=True, verbose_name='Ventaillation Hole Below Oven Is Available')),
                ('ventillation_hole_below_oven_measurements', models.CharField(max_length=350, verbose_name='Ventillation Hole Below Oven Measurements')),
                ('ventillation_hole_in_front_of_oven_is_available', models.BooleanField(default=True, verbose_name='Ventaillaiton Hole In Front Of Oven Is Available')),
                ('ventillation_hole_in_front_of_oven_measurements', models.CharField(max_length=350, verbose_name='Ventaillaiton Hole In Front Of Oven Measurements')),
                ('stabilizer_type', models.CharField(max_length=350, verbose_name='Stabilizer Type')),
                ('gas_oven_fonia_number', models.CharField(max_length=350, verbose_name='Gas Oven Fonia Number')),
                ('grill_fonia_number', models.CharField(max_length=350, verbose_name='Grill Fonia Number')),
                ('whats_done_by_the_technician', models.TextField(verbose_name="What's Done By The Technician")),
                ('gas_oven_final_condition', models.TextField(verbose_name='Gas Oven Final Condition')),
                ('client_signature', models.CharField(max_length=350, verbose_name='Client Signature')),
                ('technician_name', models.CharField(max_length=350, verbose_name='Technician Name')),
                ('notes', models.TextField(verbose_name='Notes')),
            ],
        ),
        migrations.CreateModel(
            name='HoodInstallationRequirementsForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hood_model_number', models.CharField(max_length=350, verbose_name='Hood Model Number')),
                ('hood_height', models.CharField(max_length=350, verbose_name='Hood Height')),
                ('hood_exhaust_height', models.CharField(max_length=350, verbose_name='Hood Exhaust Height')),
                ('hood_exhaust_is_straight', models.BooleanField(default=True, verbose_name='Hood Exhaust Is Straight')),
                ('notes', models.TextField(verbose_name='Notes')),
                ('whats_done_by_the_technician', models.TextField(verbose_name="What's Done By The Technician")),
                ('hood_final_condition', models.TextField(verbose_name='Hood Final Condition')),
                ('client_signature', models.CharField(max_length=350, verbose_name='Client Signature')),
                ('technician_name', models.CharField(max_length=350, verbose_name='Technician Name')),
            ],
        ),
        migrations.CreateModel(
            name='SlimHobInstallationRequirementsForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slim_hob_model_number', models.CharField(max_length=350, verbose_name='Slim Hob Model Number')),
                ('marble_dropping_hole_is_available', models.BooleanField(default=True, verbose_name='Marble Dropping Hole')),
                ('marble_dropping_hole_measurements', models.CharField(max_length=350, verbose_name='Marble Dropping Hole Measurements')),
                ('gas_type', models.CharField(max_length=350, verbose_name='Gas Type')),
                ('gas_pressure', models.CharField(max_length=350, verbose_name='Gas Pressure')),
                ('stabilizer_type', models.CharField(max_length=350, verbose_name='Stabilizer Type')),
                ('whats_done_by_the_technician', models.TextField(verbose_name="What's Done By The Technician")),
                ('slim_hob_final_condition', models.TextField(verbose_name='Slim Hob Final Condition')),
                ('client_signature', models.CharField(max_length=350, verbose_name='Client Signature')),
                ('technician_name', models.CharField(max_length=350, verbose_name='Technician Name')),
                ('notes', models.TextField(verbose_name='Notes')),
            ],
        ),
    ]
