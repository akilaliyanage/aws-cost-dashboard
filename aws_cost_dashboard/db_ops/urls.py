from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('cost/', views.get_cost_and_usage_for_current_month, name='get all demensions'),
]
