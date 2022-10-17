from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/', views.ajax_req, name='ajax'),
    
]