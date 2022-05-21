from django.db import models


class DimSuite(models.Model):
    category = models.CharField(max_length=100, default='')
    benchmark = models.CharField(max_length=100, default='')
    suite = models.CharField(max_length=300, default='')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dim_suite'


class DimDate(models.Model):
    year = models.IntegerField(default=0)
    quarter = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    full_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dim_date'


class DimCpu(models.Model):
    cpu_vendor = models.CharField(max_length=100, default='')
    cpu_name = models.CharField(max_length=400, default='')
    cpu_ghz = models.FloatField(default=0.)
    max_ghz = models.FloatField(default=0.)
    cores = models.IntegerField(default=1)
    threads_per_core = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dim_cpu'


class DimVendor(models.Model):
    vendor = models.CharField(max_length=100, default='')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dim_vendor'


class DimSystemSeries(models.Model):
    system_series = models.CharField(max_length=300, default='')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dim_system_series'


class DimSystem(models.Model):
    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='dim_system')
    vendor_name = models.CharField(max_length=100, default='')

    system_series = models.ForeignKey(DimSystemSeries, on_delete=models.CASCADE, related_name='dim_system')
    system_series_name = models.CharField(max_length=300, default='')

    system_name = models.CharField(max_length=300, default='')

    cpu = models.ForeignKey(DimCpu, on_delete=models.CASCADE, related_name='system')
    cpu_name = models.CharField(max_length=400, default='')

    chips = models.IntegerField(default=1)
    nodes = models.IntegerField(default=1)
    total_cores = models.IntegerField(default=1)

    l1_cache = models.CharField(max_length=600, default='')
    l2_cache = models.CharField(max_length=600, default='')
    l3_cache = models.CharField(max_length=600, default='')

    memory = models.CharField(max_length=600, default='')
    memory_amount = models.IntegerField(default=1)
    memory_number = models.IntegerField(default=1)

    storage_type = models.CharField(max_length=100, default='')
    storage = models.CharField(max_length=600, default='')

    os = models.CharField(max_length=600, default='')
    file_system = models.CharField(max_length=100, default='')
    jvm = models.CharField(max_length=600, default='')

    hw_avail = models.ForeignKey(DimDate, on_delete=models.CASCADE, related_name='test_info')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dim_system'
