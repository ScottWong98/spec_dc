from django.urls import path

from ads import views

urlpatterns = [
    path('build/system', views.BuildAdsSystemView.as_view(), name='build_system'),
    path('build/vendor', views.BuildAdsVendorView.as_view(), name='build_vendor'),
    path('build/benchmark', views.BuildAdsBenchmarkView.as_view(), name='build_benchmark'),
    path('build/cpu', views.BuildAdsCpuView.as_view(), name='build_cpu'),
]
