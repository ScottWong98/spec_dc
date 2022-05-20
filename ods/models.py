from django.db import models


class OdsSpecModel(models.Model):
    suite = models.CharField(verbose_name="套件名称", max_length=20, default='')
    hw_vendor = models.CharField(verbose_name="服务器厂商", max_length=100, default='')
    system_series = models.CharField(verbose_name="服务器系列", max_length=100, default='')
    result = models.FloatField(verbose_name="得分", default=0.)
    cpu_vendor = models.CharField(verbose_name="cpu 厂商", max_length=100, default='')
    cpu_name = models.CharField(verbose_name="cpu 名字", max_length=100, default='')
    cpu_ghz = models.FloatField(verbose_name="CPU GHz", default=0.)
    max_ghz = models.FloatField(verbose_name="CPU Max GHz", default=0.)
    threads_per_core = models.IntegerField(verbose_name="每个核的线程数", default=1)
    cores_per_chip = models.IntegerField(verbose_name="每个cpu的核数", default=1)
    chips = models.IntegerField(verbose_name="芯片数", default=1)
    nodes = models.IntegerField(verbose_name="节点数", default=1)
    total_cores = models.IntegerField(verbose_name="总核数", default=1)
    l1_cache = models.CharField(verbose_name="一级缓存", max_length=255, default='')
    l2_cache = models.CharField(verbose_name="二级缓存", max_length=255, default='')
    l3_cache = models.CharField(verbose_name="三级缓存", max_length=255, default='')
    memory = models.CharField(verbose_name="内存信息", max_length=255, default='')
    memory_amount = models.IntegerField(verbose_name="内存总量", default=1)
    memory_number = models.IntegerField(verbose_name="内存条数量", default=1)
    storage_type = models.CharField(verbose_name="硬盘类型", max_length=100, default='')
    storage = models.CharField(verbose_name="硬盘信息", max_length=255, default='')
    os = models.CharField(verbose_name="OS信息", max_length=255, default='')
    file_system = models.CharField(verbose_name="文件系统", max_length=100, default='')
    jvm = models.CharField(verbose_name="JVM信息", max_length=255, default='')
    url_suffix = models.CharField(verbose_name="url后缀", max_length=100, default='')
    test_date = models.DateField(verbose_name="测试日期")
    hw_avail = models.DateField(verbose_name="硬件发布时间")
    submit_quarter = models.IntegerField(verbose_name="提交时间所在季度", default=1)
    submit_year = models.IntegerField(verbose_name="提交时间所在年份", default=0)
    full_url = models.CharField(verbose_name="URL链接", max_length=100, default='')

    class Meta:
        db_table = 'ods_spec'
        verbose_name = 'spec'
        verbose_name_plural = verbose_name

