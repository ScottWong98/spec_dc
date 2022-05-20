import datetime

from django.db.models import Q, Count
from django.http import HttpResponse
from django.views import View

from dim.models import DimSuite, DimDate, DimVendor
from dwd.models import DwdTestInfo, DwdSubmitInfo
from dws.models import DwsBenchmark, DwsVendor
from spec_dc.utils import get_year_and_quarter, get_recent_n_year


class BuildDwsBenchmarkView(View):

    def get(self, request):
        self._solve()
        return HttpResponse('Build dws_benchmark View\n')

    def _solve(self):
        suites = DimSuite.objects.all()
        for suite in suites.iterator():
            print(f"--- Start {suite.suite}")
            self._get_top_1y(suite)
            self._get_top_1q(suite)
            self._get_top_y(suite)
            self._get_top(suite)

    def _get_top(self, suite):
        base_query_set = DwdTestInfo.objects.filter(
            suite_id=suite.id
        )
        self._insert_by_cpu_type(suite, base_query_set, 'all', top=-1)

    def _get_top_1y(self, suite):
        start, now = get_recent_n_year()
        base_query_set = DwdTestInfo.objects.filter(
            Q(suite_id=suite.id) & Q(test_date__full_date__range=(start, now))
        )
        self._insert_by_cpu_type(suite, base_query_set, '1y')

    def _get_top_1q(self, suite):
        cur_year, cur_quarter = get_year_and_quarter(datetime.datetime.now())
        cur_quarter -= 1
        base_query_set = DwdTestInfo.objects.filter(
            Q(suite_id=suite.id) & Q(test_date__quarter=cur_quarter) & Q(test_date__year=cur_year)
        )
        self._insert_by_cpu_type(suite, base_query_set, '1q')

    def _get_top_y(self, suite):
        years = DwdTestInfo.objects.values_list('test_date__year').distinct()
        for year in years:
            year = year[0]
            base_query_set = DwdTestInfo.objects.filter(
                Q(suite_id=suite.id) & Q(test_date__year=year)
            ).order_by('-result')

            self._insert_by_cpu_type(suite, base_query_set, 'y')

    def _insert_by_cpu_type(self, suite, base_query_set, time_level, top=3):
        query_set = base_query_set.order_by('-result')
        self._insert(suite, query_set, 'All', time_level, top)

        cpu_types = ['Intel', 'AMD', 'Huawei']
        for cpu_type in cpu_types:
            query_set = self._get_query_set_cpu_type(base_query_set, cpu_type).order_by('-result')
            self._insert(suite, query_set, cpu_type=cpu_type, time_level=time_level)

    @classmethod
    def _get_query_set_cpu_type(cls, query_set, cpu_type):
        return query_set.filter(cpu__cpu_vendor=cpu_type)

    @classmethod
    def _insert(cls, suite, query_set, cpu_type, time_level, top=3):
        idx = 1
        if top != -1:
            query_set = query_set[:top]
        total_len = len(query_set)
        for item in query_set:
            test_date_value = DimDate.objects.get(id=item.test_date_id).full_date
            DwsBenchmark.objects.get_or_create(
                suite_id=item.suite_id, suite_name=item.suite_name,
                system_id=item.system_id, system_name=item.system_name,
                vendor_id=item.vendor_id, vendor_name=item.vendor_name,
                cpu_type=cpu_type, rank_level=idx, hw_avail_id=item.hw_avail_id,
                test_date_id=item.test_date_id, test_date_value=test_date_value, time_level=time_level,
                result=item.result
            )
            print(f"[{suite.suite}] [{time_level}]: {idx} / {total_len}")
            idx += 1


class BuildDwsVendorView(View):

    def get(self, request):
        self._solve()
        return HttpResponse('Build dws_vendor View\n')

    def _solve(self):
        vendors = DimVendor.objects.all()
        for vendor in vendors.iterator():
            submit_sum_1y = self._get_submit_sum_1y(vendor)
            submit_sum_1q = self._get_submit_sum_1q(vendor)
            submit_sum = self._get_submit_sum(vendor)
            first_submit_date = self._get_first_submit_date(vendor)
            last_submit_date = self._get_last_submit_date(vendor)
            system_sum = self._get_system_sum(vendor, 'system_name')
            system_series_sum = self._get_system_sum(vendor, 'system_series')
            nt_1y = self._get_nt(vendor, '1y')
            nt_1q = self._get_nt(vendor, '1q')
            DwsVendor.objects.get_or_create(
                vendor_id=vendor.id, vendor_name=vendor.vendor,
                submit_sum_1y=submit_sum_1y, submit_sum_1q=submit_sum_1q,
                submit_sum=submit_sum, first_submit_date=first_submit_date,
                last_submit_date=last_submit_date, system_sum=system_sum,
                system_series_sum=system_series_sum, nt_1y=nt_1y, nt_1q=nt_1q
            )

    @classmethod
    def _get_submit_sum_1y(cls, vendor):
        start, now = get_recent_n_year()
        return DwdSubmitInfo.objects.filter(
            Q(vendor_id=vendor.id) & Q(submit_year=start.year)
        ).aggregate(submit_sum=Count('id')).get('submit_sum', 0)

    @classmethod
    def _get_submit_sum_1q(cls, vendor):
        year, quarter = 2022, 1
        return DwdSubmitInfo.objects.filter(
            Q(vendor_id=vendor.id) & Q(submit_year=year) & Q(submit_quarter=quarter)
        ).aggregate(submit_sum=Count('id')).get('submit_sum', 0)

    @classmethod
    def _get_submit_sum(cls, vendor):
        return DwdSubmitInfo.objects.filter(
            Q(vendor_id=vendor.id)
        ).aggregate(submit_sum=Count('id')).get('submit_sum', 0)

    @classmethod
    def _get_first_submit_date(cls, vendor):
        year, quarter = DwdSubmitInfo.objects.filter(
            vendor_id=vendor.id
        ).order_by('submit_year', 'submit_quarter').values_list('submit_year', 'submit_quarter')[0]
        month = (quarter - 1) * 3 + 1
        return datetime.date(year, month, 1)

    @classmethod
    def _get_last_submit_date(cls, vendor):
        year, quarter = DwdSubmitInfo.objects.filter(
            vendor_id=vendor.id
        ).order_by('-submit_year', '-submit_quarter').values_list('submit_year', 'submit_quarter')[0]
        month = quarter * 3
        return datetime.date(year, month, 1)

    @classmethod
    def _get_system_sum(cls, vendor, system_filed):
        return DwdSubmitInfo.objects.filter(
            vendor_id=vendor.id
        ).values(system_filed).distinct().aggregate(cnt=Count(system_filed)).get('cnt', 0)

    @classmethod
    def _get_nt(cls, vendor, time_level):
        if time_level == '1y':
            start, now = get_recent_n_year()
            return DwdTestInfo.objects.filter(
                Q(vendor_id=vendor.id) & Q(test_date__full_date__range=(start, now))
            ).aggregate(cnt=Count('id')).get('cnt', 0)
        else:
            cur_year, cur_quarter = get_year_and_quarter(datetime.datetime.now())
            cur_quarter -= 1
            return DwdTestInfo.objects.filter(
                Q(vendor_id=vendor.id) & Q(test_date__quarter=cur_quarter) & Q(test_date__year=cur_year)
            ).aggregate(cnt=Count('id')).get('cnt', 0)
