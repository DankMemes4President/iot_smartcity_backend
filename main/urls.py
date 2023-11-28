from django.urls import path
from main.views import *

urlpatterns = [
    path('clear-data/', clear_data_initiate, name="clear_data"),
    path('clear-data/status/<str:task_id>/', clear_data_status, name="clear_data_status"),
    path('generate-data/', generate_data_initiate, name="generate_data"),
    path('generate-data/status/<str:task_id>/', generate_data_status, name="generate_data"),
    path('get-results/', get_results_initiate, name="generate_data"),
    path('get-results/status/<str:task_id>/', get_results_status, name="generate_data"),
]