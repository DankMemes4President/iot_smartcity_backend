from django.urls import path
from main.views import *

urlpatterns = [
    path('simulation/', clear_data_initiate, name="clear_data"),
    path('simulation/status/<str:task_id>/', clear_data_status, name="clear_data_status"),
    # path('generate-data/', generate_data_initiate, name="generate_data"),
    # path('generate-data/status/<str:task_id>/', generate_data_status, name="generate_data"),
    path('get-results/', get_results_initiate, name="generate_data"),
    path('get-results/status/<str:task_id>/', get_results_status, name="generate_data"),
    path('park-sim/', park_sim_initiate, name="park_sim_init"),
    path('park-sim/status/<str:task_id>', park_sim_status, name="park_sim_status"),
]