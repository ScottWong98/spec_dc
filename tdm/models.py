from django.db import models

from dim.models import DimVendor, DimSystem, DimSuite, DimCpu, DimSystemSeries
from dwd.models import DwdTestInfo


class TdmVendor(models.Model):

    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='tdm_vendor')
    vendor_name = models.CharField(max_length=300, default='')

    active_score = models.FloatField(default=0.)
    submit_ratio = models.FloatField(default=0.)

    prefer_cpu_type = models.CharField(max_length=300, default='')
    cpu_sum_intel = models.IntegerField(default=0)
    cpu_sum_amd = models.IntegerField(default=0)
    cpu_sum_huawei = models.IntegerField(default=0)
    cpu_sum_other = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tdm_vendor'


class TdmSystem(models.Model):
    system = models.ForeignKey(DimSystem, on_delete=models.CASCADE, related_name='tdm_system')
    system_name = models.CharField(max_length=300, default='')

    system_series = models.ForeignKey(DimSystemSeries, on_delete=models.CASCADE, related_name='tdm_system')
    system_series_name = models.CharField(max_length=300, default='')

    vendor = models.ForeignKey(DimVendor, on_delete=models.CASCADE, related_name='tdm_system')
    vendor_name = models.CharField(max_length=100, default='')

    total_cores = models.IntegerField(default=0)
    total_threads = models.IntegerField(default=0)

    best_rank = models.IntegerField(default=0)
    best_rank_suite = models.ForeignKey(DimSuite, on_delete=models.CASCADE, related_name='tdm_system')
    best_rank_suite_name = models.CharField(max_length=300, default='')
    best_rank_total_num = models.IntegerField(default=0)

    best_rank_test = models.ForeignKey(DwdTestInfo, on_delete=models.CASCADE, related_name='tdm_system')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tdm_system'


class TdmCpu(models.Model):

    cpu = models.ForeignKey(DimCpu, on_delete=models.CASCADE, related_name='tdm_cpu')
    cpu_name = models.CharField(max_length=300, default='')
    cpu_vendor = models.CharField(max_length=100, default='')

    cpu_ghz = models.FloatField(default=0.)
    max_ghz = models.FloatField(default=0.)
    cores = models.IntegerField(default=1)
    threads_per_core = models.IntegerField(default=1)

    is_turbo = models.IntegerField(default=0)
    logical_cpus = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tdm_cpu'
