from celery.result import AsyncResult
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.simulateFlow import start_simulation, get_simulation_result


@csrf_exempt
@api_view(["GET"])
def clear_data_initiate(request):
    # print("dispatching job...")
    task = start_simulation.delay()
    # print("job dispatched...")
    return Response({"message": "Simulation started", "task": task.id, })


@csrf_exempt
@api_view(["GET"])
def clear_data_status(request, task_id):
    task = AsyncResult(task_id)
    response_data = {'status': task.status}
    if task.status == 'SUCCESS':
        response_data['data'] = task.result
    return Response(response_data)

#
# @csrf_exempt
# @api_view(["GET"])
# def generate_data_initiate(request):
#     print("generating data...")
#     task = generate_data.delay()
#     return Response({
#         "message": "Generating data",
#         "task": task.id
#     })
#
#
# @csrf_exempt
# @api_view(["GET"])
# def generate_data_status(request, task_id):
#     task = AsyncResult(task_id)
#     response_data = {'status': task.status}
#     if task.status == 'SUCCESS':
#         response_data['data'] = task.result
#     return Response(response_data)
#

@csrf_exempt
@api_view(["GET"])
def get_results_initiate(request):
    print("getting results...")
    task = get_simulation_result.delay()
    return Response({
        "message": "getting result data",
        "task": task.id
    })


@csrf_exempt
@api_view(["GET"])
def get_results_status(request, task_id):
    task = AsyncResult(task_id)
    response_data = {'status': task.status}
    if task.status == 'SUCCESS':
        response_data['data'] = task.result
    return Response(response_data)
