from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.views import exception_handler
from .serializers import TaskSerializer
from django.http import HttpResponse
from mytask.task import *
from django.http import JsonResponse
from .task import testing
from djangotask.celery import app
from collections import deque


def test(request):
    task = app.tasks.get("task1")
    # task.delay()
    task.apply_async()
    return HttpResponse("Done")



 
class TaskView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            try:
                task = app.tasks.get(name)
                task_result = task.apply_async()
                # worker_result = read_alldata_csv.apply_async(args=[name], queue=name)
                # worker_result = read_alldata_csv.delay()
                # Wait for the task to complete and get the result
                task_result = task_result.get()
                print(task_result)

                return Response({'success': True, 'output': task_result}, status=status.HTTP_200_OK)
            except requests.exceptions.RequestException as e:
                print(f'Request failed with error: {str(e)}')
                return Response({'success': False, 'error': f'Request failed with error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': False, 'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    
    
