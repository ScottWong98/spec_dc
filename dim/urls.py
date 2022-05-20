from django.urls import path

from dim import views

urlpatterns = [
    path('build', views.BuildDimView.as_view(), name='build'),
]
