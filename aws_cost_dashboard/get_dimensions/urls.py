from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('cost/', views.get_cost_and_usage_for_current_month, name='get all demensions'),
    path('past-cost/', views.get_cost_and_usage_for_past_six_months, name='get all demensions'),
    path('dims/', views.get_dimensions, name='get all demensions'),
    path('tags/', views.get_tags, name='get all demensions'),
    path('pcost/', views.get_forecats_cost, name='get all demensions'),
    path('db/', views.save_to_db, name='get all demensions'),
]
