from django.db import models

from dim.models import DimSuite, DimSystem, DimVendor, DimDate, DimCpu


class AdsBenchmark(models.Model):
    suite = models.ForeignKey(DimSuite, on_delete=models.CASCADE, related_name='ads_benchmark')
    suite_name = models.CharField(max_length=100, default='')

    system = models.ForeignKey(DimSystem, on_delete=models.CASCADE, related_name='ads_benchmark')
    system_name = models.CharField(max_length=300, default='')

    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='ads_benchmark')
    vendor_name = models.CharField(max_length=100, default='')

    cpu_type = models.CharField(max_length=10, default='')
    rank_level = models.IntegerField(default=0)

    hw_avail = models.ForeignKey(DimDate, on_delete=models.CASCADE, related_name='ads_benchmark_hw_avail')
    test_date = models.ForeignKey(DimDate, on_delete=models.CASCADE, related_name='ads_benchmark_test_date')

    test_date_value = models.DateField()

    time_level = models.CharField(max_length=10, default='')

    result = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ads_benchmark'


class AdsVendor(models.Model):

    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='ads_vendor')
    vendor_name = models.CharField(max_length=100, default='')

    submit_sum_1y = models.IntegerField(default=0)
    submit_sum_1q = models.IntegerField(default=0)

    submit_sum = models.IntegerField(default=0)

    first_submit_date = models.DateField()
    last_submit_date = models.DateField()
    system_sum = models.IntegerField(default=0)
    system_series_sum = models.IntegerField(default=0)
    nt_1y = models.IntegerField(default=0)
    nt_1q = models.IntegerField(default=0)

    active_score = models.FloatField(default=0.)
    submit_ratio = models.FloatField(default=0.)

    prefer_cpu_type = models.CharField(max_length=100, default='')
    cpu_sum_intel = models.IntegerField(default=0)
    cpu_sum_amd = models.IntegerField(default=0)
    cpu_sum_huawei = models.IntegerField(default=0)
    cpu_sum_other = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ads_vendor'


class AdsSystem(models.Model):
    system = models.ForeignKey(DimSystem, on_delete=models.CASCADE, related_name='ads_system')
    system_name = models.CharField(max_length=300, default='')
    system_series = models.CharField(max_length=300, default='')

    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='ads_system')
    vendor_name = models.CharField(max_length=100, default='')

    cpu = models.ForeignKey(DimCpu, on_delete=models.CASCADE, related_name='ads_system')

    chips = models.IntegerField(default=1)
    nodes = models.IntegerField(default=1)
    total_cores = models.IntegerField(default=0)
    total_threads = models.IntegerField(default=0)

    memory = models.CharField(max_length=255, default='')
    memory_amount = models.IntegerField(default=1)
    memory_number = models.IntegerField(default=1)

    storage_type = models.CharField(max_length=100, default='')
    storage = models.CharField(max_length=255, default='')

    os = models.CharField(max_length=255, default='')
    file_system = models.CharField(max_length=100, default='')
    jvm = models.CharField(max_length=255, default='')

    hw_avail = models.ForeignKey(DimDate, on_delete=models.CASCADE, related_name='ads_system_hw_avail')

    best_rank = models.IntegerField(default=0)
    best_rank_suite = models.ForeignKey(DimSuite, on_delete=models.CASCADE, related_name='ads_system')
    best_rank_suite_name = models.CharField(max_length=100, default='')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ads_system'


class AdsCpu(models.Model):
    cpu_vendor = models.CharField(max_length=100, default='')
    cpu_name = models.CharField(max_length=255, default='')
    cpu_ghz = models.FloatField(default=0.)
    max_ghz = models.FloatField(default=0.)
    cores = models.IntegerField(default=1)
    threads_per_core = models.IntegerField(default=1)

    is_turbo = models.BooleanField(default=False)
    logical_cpus = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ads_cpu'
