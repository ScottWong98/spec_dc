import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views import View

from dim.models import DimSuite, DimDate, DimCpu, DimVendor, DimSystem
from dwd.models import DwdTestInfo, DwdSubmitInfo
from ods.models import OdsSpecModel


class BuildDimView(View):

    def get(self, request: WSGIRequest):
        self._solve()
        return HttpResponse('Build Dim View\n')

    def _solve(self):
        query_set = OdsSpecModel.objects.all()
        idx = 1
        total_num = len(query_set)
        for spec_model in query_set.iterator():
            self._build_dim(spec_model)
            if idx % 50 == 0:
                print(f"Status: {idx} / {total_num}")
            idx += 1

    def _build_dim(self, spec_model: OdsSpecModel):
        suite = self._process_suite(spec_model.suite)
        test_date = self._process_date(spec_model.test_date)
        hw_avail = self._process_date(spec_model.hw_avail)
        cpu = self._process_cpu(
            spec_model.cpu_vendor, spec_model.cpu_name, spec_model.cpu_ghz,
            spec_model.max_ghz, spec_model.cores_per_chip, spec_model.threads_per_core,
        )
        vendor = self._process_vendor(spec_model.hw_vendor)
        system_name = f"{spec_model.system_series} ({spec_model.cpu_name})"
        system = self._process_system(
            vendor.id, spec_model.hw_vendor, spec_model.system_series, system_name,
            cpu.id, spec_model.chips, spec_model.nodes, spec_model.total_cores,
            spec_model.l1_cache, spec_model.l2_cache, spec_model.l3_cache,
            spec_model.memory, spec_model.memory_number, spec_model.memory_amount,
            spec_model.storage_type, spec_model.storage, spec_model.os,
            spec_model.file_system, spec_model.jvm, hw_avail.id
        )

        DwdTestInfo.objects.get_or_create(
            vendor_id=vendor.id, vendor_name=vendor.vendor, system_id=system.id,
            system_series=system.system_series, system_name=system_name,
            cpu_id=cpu.id, chips=system.chips, nodes=system.chips,
            total_cores=system.total_cores, l1_cache=system.l1_cache,
            l2_cache=system.l2_cache, l3_cache=system.l3_cache, memory=system.memory,
            memory_amount=system.memory_amount, memory_number=system.memory_number,
            storage_type=system.storage_type, storage=system.storage, os=system.os,
            file_system=system.file_system, jvm=system.jvm, hw_avail_id=hw_avail.id,
            result=spec_model.result, suite_id=suite.id, suite_name=suite.suite,
            test_date_id=test_date.id
        )
        DwdSubmitInfo.objects.get_or_create(
            vendor_id=vendor.id, vendor_name=vendor.vendor, system_id=system.id,
            system_series=system.system_series, system_name=system.system_name,
            suite_id=suite.id, suite_name=suite.suite, submit_year=spec_model.submit_year,
            submit_quarter=spec_model.submit_quarter
        )

    @classmethod
    def _process_system(cls, vendor_id, hw_vendor, system_series, system_name, cpu_id, chips,
                        nodes, total_cores, l1_cache, l2_cache, l3_cache, memory,
                        memory_number, memory_amount, storage_type, storage, os,
                        file_system, jvm, hw_avail_id):
        obj, created = DimSystem.objects.get_or_create(
            vendor_id=vendor_id, vendor_name=hw_vendor, system_series=system_series,
            system_name=system_name, cpu_id=cpu_id, chips=chips, nodes=nodes, total_cores=total_cores,
            l1_cache=l1_cache, l2_cache=l2_cache, l3_cache=l3_cache, memory=memory,
            memory_number=memory_number, memory_amount=memory_amount, storage_type=storage_type,
            storage=storage, os=os, file_system=file_system, jvm=jvm, hw_avail_id=hw_avail_id,
        )
        return obj

    @classmethod
    def _process_vendor(cls, hw_vendor):
        obj, created = DimVendor.objects.get_or_create(vendor=hw_vendor)
        return obj

    @classmethod
    def _process_cpu(cls, cpu_vendor, cpu_name, cpu_ghz, max_ghz, cores, threads_per_core):
        obj, created = DimCpu.objects.get_or_create(
            cpu_vendor=cpu_vendor, cpu_name=cpu_name, cpu_ghz=cpu_ghz, max_ghz=max_ghz,
            cores=cores, threads_per_core=threads_per_core
        )
        return obj

    def _process_suite(self, suite):
        category, benchmark = self._parse_suite(suite)
        obj, created = DimSuite.objects.get_or_create(category=category, benchmark=benchmark, suite=suite)
        return obj

    def _process_date(self, date_str):
        year, quarter, month, day = self._parse_date(date_str)
        obj, created = DimDate.objects.get_or_create(year=year, quarter=quarter, month=month, day=day,
                                                     full_date=date_str)
        return obj

    @classmethod
    def _parse_suite(cls, suite):
        if 'SPECfp' in suite or 'SPECint' in suite:
            category = 'cpu'
            benchmark = 'cpu2006'
        elif '2017' in suite:
            category = 'cpu'
            benchmark = 'cpu2017'
        elif 'jbb2015' in suite:
            category = 'java'
            benchmark = 'jbb2015'
        elif 'jvm2008' in suite:
            category = 'java'
            benchmark = 'jvm2008'
        else:
            category = 'power'
            benchmark = 'ssj2008'
        return category, benchmark

    @classmethod
    def _parse_date(cls, date_str: datetime.date):
        year = int(date_str.strftime('%Y'))
        month = int(date_str.strftime('%m'))
        day = int(date_str.strftime('%d'))
        quarter = (month - 1) // 3 + 1
        return year, quarter, month, day
