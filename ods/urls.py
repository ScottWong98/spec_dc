from django.urls import path

from ods import views

urlpatterns = [
    path('load/', views.LoadView.as_view(), name='load'),
]
