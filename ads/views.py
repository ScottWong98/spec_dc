from django.http import HttpResponse
from django.views import View

from ads.models import AdsBenchmark, AdsVendor, AdsSystem, AdsCpu
from dim.models import DimSystem
from dws.models import DwsBenchmark, DwsVendor
from tdm.models import TdmVendor, TdmSystem, TdmCpu


class BuildAdsBenchmarkView(View):
    def get(self, request):
        self._solve()
        return HttpResponse('Build ADS Benchmark View\n')

    @classmethod
    def _solve(cls):
        bms = DwsBenchmark.objects.all()
        print("--- Start build ads_benchmark ---")
        idx, total_len = 1, len(bms)
        for bm in bms.iterator():
            AdsBenchmark.objects.get_or_create(
                suite_id=bm.suite_id, suite_name=bm.suite_name, system_id=bm.system_id,
                system_name=bm.system_name, vendor_id=bm.vendor_id, vendor_name=bm.vendor_name,
                cpu_type=bm.cpu_type, rank_level=bm.rank_level, hw_avail_id=bm.hw_avail_id,
                test_date_id=bm.test_date_id, test_date_value=bm.test_date_value,
                time_level=bm.time_level, result=bm.result,
            )
            print(f"Build ads_benchmark: {idx} / {total_len}")
            idx += 1


class BuildAdsVendorView(View):
    def get(self, request):
        self._solve()
        return HttpResponse('Build ADS Vendor View\n')

    @classmethod
    def _solve(cls):
        dws_vendors = DwsVendor.objects.all()
        print("--- Start build ads_vendor ---")
        idx, total_len = 1, len(dws_vendors)
        for dws_vendor in dws_vendors.iterator():
            tdm_vendor = TdmVendor.objects.get(vendor_id=dws_vendor.vendor_id)
            AdsVendor.objects.get_or_create(
                vendor_id=dws_vendor.vendor_id, vendor_name=dws_vendor.vendor_name, submit_sum_1y=dws_vendor.submit_sum_1y,
                submit_sum_1q=dws_vendor.submit_sum_1q, submit_sum=dws_vendor.submit_sum,
                first_submit_date=dws_vendor.first_submit_date, last_submit_date=dws_vendor.last_submit_date,
                system_sum=dws_vendor.system_sum, system_series_sum=dws_vendor.system_series_sum,
                nt_1y=dws_vendor.nt_1y, nt_1q=dws_vendor.nt_1q,
                active_score=tdm_vendor.active_score, submit_ratio=tdm_vendor.submit_ratio,
                prefer_cpu_type=tdm_vendor.prefer_cpu_type, cpu_sum_intel=tdm_vendor.cpu_sum_intel,
                cpu_sum_amd=tdm_vendor.cpu_sum_amd, cpu_sum_huawei=tdm_vendor.cpu_sum_huawei,
                cpu_sum_other=tdm_vendor.cpu_sum_other,
            )
            print(f"Build ads_vendor: {idx} / {total_len}")
            idx += 1


class BuildAdsSystemView(View):
    def get(self, request):
        self._solve()
        return HttpResponse('Build ADS System View\n')

    @classmethod
    def _solve(cls):
        systems = DimSystem.objects.all()
        print(f"--- Start Build ads_system ---")
        idx, total_len = 1, len(systems)
        for system in systems.iterator():
            tdm_system = TdmSystem.objects.get(id=system.id)
            AdsSystem.objects.get_or_create(
                system_id=system.id, system_name=system.system_name, system_series=system.system_series,
                vendor_id=system.vendor_id, vendor_name=system.vendor_name, cpu_id=system.cpu_id,
                chips=system.chips, nodes=system.nodes, total_cores=system.total_cores,
                total_threads=tdm_system.total_threads, memory=system.memory,
                memory_amount=system.memory_amount, memory_number=system.memory_number,
                storage_type=system.storage_type, storage=system.storage,
                os=system.os, file_system=system.file_system, jvm=system.jvm,
                hw_avail_id=system.hw_avail_id, best_rank=tdm_system.best_rank,
                best_rank_suite_id=tdm_system.best_rank_suite_id,
                best_rank_suite_name=tdm_system.best_rank_suite_name,
            )
            print(f"Build ads_system: {idx} / {total_len}")
            idx += 1


class BuildAdsCpuView(View):
    def get(self, request):
        self._solve()
        return HttpResponse('Build ADS CPU View\n')

    @classmethod
    def _solve(cls):
        print("--- Start Build ads_cpu ---")
        cpus = TdmCpu.objects.all()
        idx, total_len = 1, len(cpus)
        for cpu in cpus.iterator():
            AdsCpu.objects.get_or_create(
                cpu_vendor=cpu.cpu_vendor, cpu_name=cpu.cpu_name,
                cpu_ghz=cpu.cpu_ghz, max_ghz=cpu.max_ghz,
                cores=cpu.cores, threads_per_core=cpu.threads_per_core,
                is_turbo=cpu.is_turbo, logical_cpus=cpu.logical_cpus,
            )
            print(f"Build ads_cpu: {idx} / {total_len}")
            idx += 1
