from django.db import models

from dim.models import DimVendor, DimSystem, DimCpu, DimSuite, DimDate


class DwdTestInfo(models.Model):
    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='test_info')
    vendor_name = models.CharField(max_length=100, default='')

    system = models.ForeignKey(DimSystem, on_delete=models.CASCADE, related_name='test_info')
    system_series = models.CharField(max_length=100, default='')
    system_name = models.CharField(max_length=300, default='')

    cpu = models.ForeignKey(DimCpu, on_delete=models.CASCADE, related_name='test_info')

    chips = models.IntegerField(default=1)
    nodes = models.IntegerField(default=1)
    total_cores = models.IntegerField(default=1)

    l1_cache = models.CharField(max_length=255, default='')
    l2_cache = models.CharField(max_length=255, default='')
    l3_cache = models.CharField(max_length=255, default='')

    memory = models.CharField(max_length=255, default='')
    memory_amount = models.IntegerField(default=1)
    memory_number = models.IntegerField(default=1)

    storage_type = models.CharField(max_length=100, default='')
    storage = models.CharField(max_length=255, default='')

    os = models.CharField(max_length=255, default='')
    file_system = models.CharField(max_length=100, default='')
    jvm = models.CharField(max_length=255, default='')

    hw_avail = models.ForeignKey(DimDate, on_delete=models.CASCADE, related_name='test_info_hw_avail')

    result = models.FloatField()
    suite = models.ForeignKey(DimSuite, on_delete=models.CASCADE, related_name='test_info')
    suite_name = models.CharField(max_length=100, default='')
    test_date = models.ForeignKey(DimDate, on_delete=models.CASCADE, related_name='test_info_test_date')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dwd_test_info'


class DwdSubmitInfo(models.Model):
    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='submit_info')
    vendor_name = models.CharField(max_length=100, default=1)
    system = models.ForeignKey(DimSystem, on_delete=models.CASCADE, related_name='submit_info')
    system_series = models.CharField(max_length=100, default='')
    system_name = models.CharField(max_length=300, default='')

    suite = models.ForeignKey(DimSuite, on_delete=models.CASCADE, related_name='submit_info')
    suite_name = models.CharField(max_length=100, default='')

    submit_year = models.IntegerField(default=0)
    submit_quarter = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dwd_submit_info'
