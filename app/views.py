from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from dim.models import DimSystem, DimVendor, DimSuite
from dwd.models import DwdTestInfo
from dws.models import DwsBenchmark
from tdm.models import TdmSystem


def system_all(request):
    systems = DimSystem.objects.all().order_by('-hw_avail__full_date')
    paginator = Paginator(systems, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'systems_num': len(systems), 'systems': page_obj})


def system_detail(request, pk):
    system = DimSystem.objects.get(id=pk)
    tdm_system = TdmSystem.objects.get(Q(system_id=pk) & Q())
    tests = system.test_info.all()
    print(tests[0].dws_benchmark.values('rank_level', 'total_test'))
    return render(request, 'system_detail.html', {
        'system': system,
        'tdm_system': tdm_system,
        'tests': tests,
    })


def search(request):
    keywords = request.GET.get('keywords')
    print(request.GET)
    print(keywords)
    systems = DimSystem.objects.none()
    if keywords is not None and len(keywords):
        keywords_list = keywords.split()
        for keyword in keywords_list:
            print(keyword)
            res = DimSystem.objects.filter(Q(system_name__icontains=keyword))
            if len(res):
                if len(systems) == 0:
                    systems = res
                else:
                    systems = systems & res

    paginator = Paginator(systems, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search_result.html', {'systems_num': len(systems), 'systems': page_obj})


def vendor_all(request):
    vendors = DimVendor.objects.all()
    return render(request, 'vendor.html', {'vendors': vendors})


def vendor_detail(request, pk):
    vendor = DimVendor.objects.get(id=pk)
    systems = DimSystem.objects.filter(vendor_id=pk).order_by('-hw_avail__full_date')
    paginator = Paginator(systems, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'vendor_detail.html', {'systems_num': len(systems), 'vendor': vendor, 'systems': page_obj})


def benchmark_detail(request, pk):
    suite = DimSuite.objects.get(id=pk)
    bms = DwsBenchmark.objects.filter(
        Q(suite_id=pk) & Q(cpu_type='All') & Q(time_level='all')
    ).order_by('rank_level')
    paginator = Paginator(bms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bm_detail.html',
                  {'tests': page_obj, 'suite_name': suite.suite, 'tests_num': len(bms)})
