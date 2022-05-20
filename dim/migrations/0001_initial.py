# Generated by Django 3.2.5 on 2022-05-20 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DimCpu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_vendor', models.CharField(default='', max_length=100)),
                ('cpu_name', models.CharField(default='', max_length=255)),
                ('cpu_ghz', models.FloatField(default=0.0)),
                ('max_ghz', models.FloatField(default=0.0)),
                ('cores', models.IntegerField(default=1)),
                ('threads_per_core', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'dim_cpu',
            },
        ),
        migrations.CreateModel(
            name='DimDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=0)),
                ('quarter', models.IntegerField(default=0)),
                ('month', models.IntegerField(default=0)),
                ('day', models.IntegerField(default=0)),
                ('full_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'dim_date',
            },
        ),
        migrations.CreateModel(
            name='DimSuite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=100)),
                ('benchmark', models.CharField(default='', max_length=100)),
                ('suite', models.CharField(default='', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'dim_suite',
            },
        ),
        migrations.CreateModel(
            name='DimVendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(default='', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'dim_vendor',
            },
        ),
        migrations.CreateModel(
            name='DimSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(default='', max_length=100)),
                ('system_series', models.CharField(default='', max_length=100)),
                ('system_name', models.CharField(default='', max_length=300)),
                ('chips', models.IntegerField(default=1)),
                ('nodes', models.IntegerField(default=1)),
                ('total_cores', models.IntegerField(default=1)),
                ('l1_cache', models.CharField(default='', max_length=255)),
                ('l2_cache', models.CharField(default='', max_length=255)),
                ('l3_cache', models.CharField(default='', max_length=255)),
                ('memory', models.CharField(default='', max_length=255)),
                ('memory_amount', models.IntegerField(default=1)),
                ('memory_number', models.IntegerField(default=1)),
                ('storage_type', models.CharField(default='', max_length=100)),
                ('storage', models.CharField(default='', max_length=255)),
                ('os', models.CharField(default='', max_length=255)),
                ('file_system', models.CharField(default='', max_length=100)),
                ('jvm', models.CharField(default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cpu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system', to='dim.dimcpu')),
                ('hw_avail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_info', to='dim.dimdate')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system', to='dim.dimvendor')),
            ],
            options={
                'db_table': 'dim_system',
            },
        ),
    ]
