# Generated by Django 3.2.5 on 2021-07-14 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Custody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custody_name', models.CharField(max_length=350, verbose_name='Custody Name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Custody',
                'verbose_name_plural': 'Custodies',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warehouse_name', models.CharField(max_length=350, verbose_name='Warehouse Name')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Added at')),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Assigned To')),
            ],
            options={
                'verbose_name': 'Warehouse',
                'verbose_name_plural': 'Warehouses',
            },
        ),
        migrations.CreateModel(
            name='SparePart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spare_part_model_number', models.CharField(max_length=350, verbose_name='Spare Part Model')),
                ('spare_part_img', models.ImageField(upload_to='Spare_Parts_Imgs', verbose_name='Spare Part Img')),
                ('spare_part_price', models.FloatField(default=0.0, verbose_name='Spare Part Price')),
                ('available_qty', models.IntegerField(verbose_name='Available QTY')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Added at')),
                ('related_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Storage.warehouse', verbose_name='Related Warehouse')),
            ],
            options={
                'verbose_name': 'Spare Part',
                'verbose_name_plural': 'Spare Parts',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=350, verbose_name='Brand')),
                ('category', models.CharField(max_length=350, verbose_name='Category')),
                ('item_model_number', models.CharField(max_length=350, verbose_name='Item Model Number')),
                ('item_img', models.ImageField(upload_to='Items_Imgs', verbose_name='Item Img')),
                ('main_dimension', models.CharField(max_length=350, verbose_name='Main Dimension')),
                ('cut_off_dimension', models.CharField(max_length=350, verbose_name='Cutt off Dimension')),
                ('warranty_coverage', models.IntegerField(verbose_name='Warranty Coverage')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Added at')),
                ('related_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Storage.warehouse', verbose_name='Related Warehouse')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='CustodySparepart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_qty', models.IntegerField(verbose_name='Assigned Qty')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('assigned_sparepart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Storage.sparepart', verbose_name='Assigned Sparepart')),
                ('related_custody', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Storage.custody', verbose_name='Related Custody')),
            ],
            options={
                'verbose_name': 'Custody Sparepart',
                'verbose_name_plural': 'Custodies Spareparts',
            },
        ),
    ]
