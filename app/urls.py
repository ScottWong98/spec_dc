from django.urls import path

from app import views

app_name = 'app'

urlpatterns = [
    path('', views.system_all, name='index'),
    path('search', views.search, name='search'),
    path('vendor', views.vendor_all, name='vendor'),
    path('vendor/<int:pk>', views.vendor_detail, name='vendor_detail'),
    path('system/<int:pk>', views.system_detail, name='system_detail'),
    path('benchmark/<int:pk>', views.benchmark_detail, name='benchmark_detail'),
]
