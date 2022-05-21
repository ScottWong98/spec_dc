# Generated by Django 3.2.5 on 2022-05-21 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dim', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdsCpu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_vendor', models.CharField(default='', max_length=100)),
                ('cpu_name', models.CharField(default='', max_length=255)),
                ('cpu_ghz', models.FloatField(default=0.0)),
                ('max_ghz', models.FloatField(default=0.0)),
                ('cores', models.IntegerField(default=1)),
                ('threads_per_core', models.IntegerField(default=1)),
                ('is_turbo', models.BooleanField(default=False)),
                ('logical_cpus', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ads_cpu',
            },
        ),
        migrations.CreateModel(
            name='AdsVendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(default='', max_length=100)),
                ('submit_sum_1y', models.IntegerField(default=0)),
                ('submit_sum_1q', models.IntegerField(default=0)),
                ('submit_sum', models.IntegerField(default=0)),
                ('first_submit_date', models.DateField()),
                ('last_submit_date', models.DateField()),
                ('system_sum', models.IntegerField(default=0)),
                ('system_series_sum', models.IntegerField(default=0)),
                ('nt_1y', models.IntegerField(default=0)),
                ('nt_1q', models.IntegerField(default=0)),
                ('active_score', models.FloatField(default=0.0)),
                ('submit_ratio', models.FloatField(default=0.0)),
                ('prefer_cpu_type', models.CharField(default='', max_length=100)),
                ('cpu_sum_intel', models.IntegerField(default=0)),
                ('cpu_sum_amd', models.IntegerField(default=0)),
                ('cpu_sum_huawei', models.IntegerField(default=0)),
                ('cpu_sum_other', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_vendor', to='dim.dimvendor')),
            ],
            options={
                'db_table': 'ads_vendor',
            },
        ),
        migrations.CreateModel(
            name='AdsSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_name', models.CharField(default='', max_length=300)),
                ('system_series', models.CharField(default='', max_length=300)),
                ('vendor_name', models.CharField(default='', max_length=100)),
                ('chips', models.IntegerField(default=1)),
                ('nodes', models.IntegerField(default=1)),
                ('total_cores', models.IntegerField(default=0)),
                ('total_threads', models.IntegerField(default=0)),
                ('memory', models.CharField(default='', max_length=255)),
                ('memory_amount', models.IntegerField(default=1)),
                ('memory_number', models.IntegerField(default=1)),
                ('storage_type', models.CharField(default='', max_length=100)),
                ('storage', models.CharField(default='', max_length=255)),
                ('os', models.CharField(default='', max_length=255)),
                ('file_system', models.CharField(default='', max_length=100)),
                ('jvm', models.CharField(default='', max_length=255)),
                ('best_rank', models.IntegerField(default=0)),
                ('best_rank_suite_name', models.CharField(default='', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('best_rank_suite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_system', to='dim.dimsuite')),
                ('cpu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_system', to='dim.dimcpu')),
                ('hw_avail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_system_hw_avail', to='dim.dimdate')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_system', to='dim.dimsystem')),
                ('test_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_system_test_date', to='dim.dimdate')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_system', to='dim.dimvendor')),
            ],
            options={
                'db_table': 'ads_system',
            },
        ),
        migrations.CreateModel(
            name='AdsBenchmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suite_name', models.CharField(default='', max_length=100)),
                ('system_name', models.CharField(default='', max_length=300)),
                ('vendor_name', models.CharField(default='', max_length=100)),
                ('cpu_type', models.CharField(default='', max_length=10)),
                ('rank_level', models.IntegerField(default=0)),
                ('test_date_value', models.DateField()),
                ('time_level', models.CharField(default='', max_length=10)),
                ('result', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hw_avail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_benchmark_hw_avail', to='dim.dimdate')),
                ('suite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_benchmark', to='dim.dimsuite')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_benchmark', to='dim.dimsystem')),
                ('test_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_benchmark_test_date', to='dim.dimdate')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_benchmark', to='dim.dimvendor')),
            ],
            options={
                'db_table': 'ads_benchmark',
            },
        ),
    ]
