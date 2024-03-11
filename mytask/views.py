from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import TaskSerializer
from django.http import HttpResponse
from mytask.task import *
from django.http import JsonResponse
from djangotask.celery import app
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render

def index(request):
    context = {'name': 'World'}
    return render(request, 'index.html', context)

# API endpoint http://127.0.0.1:8000/api/task/
class TaskView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            try:
                name = serializer.validated_data['name']
                # Get task with provided name 
                task = app.tasks.get(name)
                task_result = task.apply_async()
                task_result_value = task_result.get()
                print(task_result_value)
                return Response({'success': True, 'output': task_result_value}, status=status.HTTP_200_OK)
            except requests.exceptions.RequestException as e:
                print(f'Request failed with error: {str(e)}')
                return Response({'success': False, 'error': f'Request failed with error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': False, 'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    
    
def test(request):
    task = app.tasks.get("testing")
    # task.delay()
    task_result = task.apply_async()
    task_result = task_result.get()
    print(task_result)
    return HttpResponse("Done")

@csrf_exempt
def hello(request):
    if request.method == 'POST':
        try:
            # Get the JSON data from the request body
            data = json.loads(request.body)
            name = data.get('name', '')
            # task = app.tasks.get(name)
            # print(task)
            # task_result = task.apply_async()
            # print(task_result)
            response_data = {'output': name}
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
