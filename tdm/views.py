import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'spec_dc.settings'
django.setup()

from django.db.models import Sum, Count, F

from dim.models import DimVendor, DimSystem, DimCpu
from dwd.models import DwdTestInfo
from dws.models import DwsVendor
from tdm.models import TdmVendor, TdmSystem, TdmCpu


class BuildTdmVendor:
    def run(self):
        self._solve()

    def _solve(self):
        print(f"--- Start build tdm_vendor ---")
        vendors = DimVendor.objects.all()
        for vendor in vendors.iterator():
            vendor_name = vendor.vendor
            active_score = self._get_active_score(vendor)
            submit_ratio = self._get_submit_ratio(vendor)
            prefer_cpu_type, cpu_sum_intel, cpu_sum_amd, cpu_sum_huawei, cpu_sum_other = self._get_cpu_info(vendor)
            TdmVendor.objects.get_or_create(
                vendor_id=vendor.id, vendor_name=vendor_name, active_score=active_score,
                submit_ratio=submit_ratio, prefer_cpu_type=prefer_cpu_type, cpu_sum_intel=cpu_sum_intel,
                cpu_sum_amd=cpu_sum_amd, cpu_sum_huawei=cpu_sum_huawei, cpu_sum_other=cpu_sum_other,
            )

    @classmethod
    def _get_active_score(cls, vendor):
        d = DwsVendor.objects.filter(
            vendor_id=vendor.id
        ).values('submit_sum', 'first_submit_date', 'last_submit_date')[0]
        score = d['submit_sum'] / (d['last_submit_date'] - d['first_submit_date']).days
        return score

    @classmethod
    def _get_submit_ratio(cls, vendor):
        submit_sum = DwsVendor.objects.filter(
            vendor_id=vendor.id
        ).values_list('submit_sum')[0][0]
        all_submit = DwsVendor.objects.aggregate(cnt=Sum('submit_sum')).get('cnt', 1)
        return submit_sum / all_submit

    @classmethod
    def _get_cpu_info(cls, vendor):
        res = list(DwdTestInfo.objects.filter(
            vendor_id=vendor.id
        ).values('cpu__cpu_vendor').annotate(cnt=Count('id')).order_by('-cnt'))
        prefer_cpu_type = res[0].get('cpu__cpu_vendor', '')
        d = {
            item['cpu__cpu_vendor'].lower(): item['cnt']
            for item in res
        }
        cpu_sum_intel, cpu_sum_amd, cpu_sum_huawei, cpu_sum_other = 0, 0, 0, 0
        if 'intel' in d:
            cpu_sum_intel = d['intel']
        if 'amd' in d:
            cpu_sum_amd = d['amd']
        if 'huawei' in d:
            cpu_sum_huawei = d['huawei']
        if 'other' in d:
            cpu_sum_other = d['other']
        return prefer_cpu_type, cpu_sum_intel, cpu_sum_amd, cpu_sum_huawei, cpu_sum_other


class BuildTdmSystem:
    def run(self):
        self._solve()

    def _solve(self):
        print(f"--- Start build tdm_system ---")
        systems = DimSystem.objects.all()
        idx = 1
        total_len = len(systems)
        for system in systems.iterator():
            total_cores, total_threads = self._get_total_cores_and_threads(system)
            best_rank, best_rank_suite_id, best_rank_suite_name, best_rank_total_num, best_rank_test_id = \
                self._get_best_rank(system)
            TdmSystem.objects.get_or_create(
                system_id=system.id, system_name=system.system_name, system_series_id=system.system_series_id,
                vendor_id=system.vendor_id, vendor_name=system.vendor_name, total_cores=total_cores,
                total_threads=total_threads,
                best_rank=best_rank, best_rank_suite_id=best_rank_suite_id, best_rank_suite_name=best_rank_suite_name,
                best_rank_total_num=best_rank_total_num, best_rank_test_id=best_rank_test_id
            )
            print(f"Status: {idx} / {total_len}")
            idx += 1

    @classmethod
    def _get_best_rank(cls, system):
        d = DimSystem.objects.get(id=system.id).dws_benchmark.values(
            'test_info_id', 'rank_level', 'suite_name', 'suite_id', 'total_test'
        ).order_by('rank_level')[0]
        return d['rank_level'], d['suite_id'], d['suite_name'], d['total_test'], d['test_info_id']

    @classmethod
    def _get_total_cores_and_threads(cls, system):
        d = DimSystem.objects.filter(id=system.id).values('total_cores', threads_per_core=F('cpu__threads_per_core'))[0]
        total_cores = d['total_cores']
        return total_cores, total_cores * d['threads_per_core']


class BuildTdmCpu:
    def run(self):
        self._solve()

    def _solve(self):
        print(f"--- Start build tdm_cpu ---")
        cpus = DimCpu.objects.all()
        for cpu in cpus.iterator():
            is_turbo = self._get_is_turbo(cpu)
            logical_cpus = self._get_logical_cpus(cpu)
            TdmCpu.objects.get_or_create(
                cpu_id=cpu.id, cpu_name=cpu.cpu_name, cpu_vendor=cpu.cpu_vendor,
                cpu_ghz=cpu.cpu_ghz, max_ghz=cpu.max_ghz, cores=cpu.cores,
                threads_per_core=cpu.threads_per_core, is_turbo=is_turbo,
                logical_cpus=logical_cpus,
            )

    @classmethod
    def _get_is_turbo(cls, cpu):
        cpu_ghz, max_ghz = DimCpu.objects.filter(id=cpu.id).values_list('cpu_ghz', 'max_ghz')[0]
        return max_ghz > cpu_ghz

    @classmethod
    def _get_logical_cpus(cls, cpu):
        cores, threads_per_cores = DimCpu.objects.filter(id=cpu.id).values_list('cores', 'threads_per_core')[0]
        return cores * threads_per_cores


def main():
    build_tdm_vendor = BuildTdmVendor()
    build_tdm_system = BuildTdmSystem()
    build_tdm_cpu = BuildTdmCpu()

    # build_tdm_vendor.run()
    # build_tdm_system.run()
    build_tdm_cpu.run()


if __name__ == '__main__':
    main()
