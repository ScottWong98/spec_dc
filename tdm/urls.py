from django.urls import path

from tdm import views

urlpatterns = [
    path('build_vendor', views.BuildTdmVendorView.as_view(), name='build_vendor'),
    path('build_system', views.BuildTdmSystemView.as_view(), name='build_system'),
    path('build_cpu', views.BuildTdmCpuView.as_view(), name='build_cpu'),
]
