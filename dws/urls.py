from django.urls import path

from dws import views

urlpatterns = [
    path('build_bm', views.BuildDwsBenchmarkView.as_view(), name='build_bm'),
    path('build_vendor', views.BuildDwsVendorView.as_view(), name='build_vendor'),
]
