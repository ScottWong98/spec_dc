from django.db import models

from dim.models import DimVendor, DimSystem, DimCpu, DimSuite, DimDate, DimSystemSeries


class DwdTestInfo(models.Model):
    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='test_info')
    vendor_name = models.CharField(max_length=300, default='')

    system = models.ForeignKey(DimSystem, on_delete=models.CASCADE, related_name='test_info')
    system_name = models.CharField(max_length=400, default='')

    system_series = models.ForeignKey(DimSystemSeries, on_delete=models.CASCADE, related_name='test_info')
    system_series_name = models.CharField(max_length=300, default='')

    cpu = models.ForeignKey(DimCpu, on_delete=models.CASCADE, related_name='test_info')
    cpu_name = models.CharField(max_length=300, default='')

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

    hw_avail = models.ForeignKey(DimDate, on_delete=models.CASCADE, related_name='test_info_hw_avail')

    result = models.FloatField()
    suite = models.ForeignKey(DimSuite, on_delete=models.CASCADE, related_name='test_info')
    suite_name = models.CharField(max_length=200, default='')
    test_date = models.ForeignKey(DimDate, on_delete=models.CASCADE, related_name='test_info_test_date')

    url_suffix = models.CharField(max_length=600, default='')
    full_url = models.CharField(max_length=600, default='')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dwd_test_info'


class DwdSubmitInfo(models.Model):
    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='submit_info')
    vendor_name = models.CharField(max_length=100, default=1)

    system = models.ForeignKey(DimSystem, on_delete=models.CASCADE, related_name='submit_info')
    system_name = models.CharField(max_length=300, default='')

    system_series = models.ForeignKey(DimSystemSeries, on_delete=models.CASCADE, related_name='submit_info')
    system_series_name = models.CharField(max_length=100, default='')

    suite = models.ForeignKey(DimSuite, on_delete=models.CASCADE, related_name='submit_info')
    suite_name = models.CharField(max_length=100, default='')

    submit_year = models.IntegerField(default=0)
    submit_quarter = models.IntegerField(default=0)

    url_suffix = models.CharField(max_length=600, default='')
    full_url = models.CharField(max_length=600, default='')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dwd_submit_info'
