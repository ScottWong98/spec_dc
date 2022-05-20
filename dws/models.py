from django.db import models

from dim.models import DimSuite, DimSystem, DimVendor, DimDate


class DwsBenchmark(models.Model):
    suite = models.ForeignKey(DimSuite, on_delete=models.CASCADE, related_name='dws_benchmark')
    suite_name = models.CharField(max_length=100, default='')

    system = models.ForeignKey(DimSystem, on_delete=models.CASCADE, related_name='dws_benchmark')
    system_name = models.CharField(max_length=300, default='')

    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='dws_benchmark')
    vendor_name = models.CharField(max_length=100, default='')

    cpu_type = models.CharField(max_length=10, default='')
    rank_level = models.IntegerField(default=0)

    hw_avail = models.ForeignKey(DimDate, on_delete=models.CASCADE, related_name='dws_benchmark_hw_avail')
    test_date = models.ForeignKey(DimDate, on_delete=models.CASCADE, related_name='dws_benchmark_test_date')

    test_date_value = models.DateField()

    time_level = models.CharField(max_length=10, default='')

    result = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dws_benchmark'


class DwsVendor(models.Model):
    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='dws_vendor')
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

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dws_vendor'
