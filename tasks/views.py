from django.shortcuts import render

# Views
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate

# Time
from django.utils.timezone import now


# Excempt csrf token
from django.views.decorators.csrf import csrf_exempt

# database
from .models import Task


# Custom imports
from utilities.validators import validate_task_inputs
from utilities.utils import handle_task_creation_or_update
from utilities.decorators import token_required


# VIEWS
@csrf_exempt
@token_required
def task_manager(request: HttpRequest) -> JsonResponse:
    print('request.user', type(request.user))
    method = request.method

    if method not in ['GET', 'POST']:
        return JsonResponse({
            'error': 'Method Not Allowed',
            'message': f'The HTTP method {method} is not allowed for this endpoint.'
        }, status=405)

    try: 
        if method == 'GET':
            
            all_tasks = Task.objects.all()
            print('all tasks', all_tasks)
            task_list = []

            for task in all_tasks:
                task_list.append(
                    {
                        'id': task.pk,
                        'title': task.title,
                        'description': task.description,
                        'status': task.status,
                        'owner': task.owner.pk
                    }
                )

            return JsonResponse({'tasks': task_list}, status=200)

        # ELSE POST METHOD.
        return handle_task_creation_or_update(request, 'Task successfully created', 201)

    except Exception as e:
        # Handle any unexpected exceptions
        return JsonResponse({
            'error': 'Server Error',
            'message': str(e)  
        }, status=500)
    

@csrf_exempt
@token_required
def task_detail(request, task_id):

    method = request.method 
    
    try:

        if method not in ['PUT', 'DELETE', 'GET']:
            return JsonResponse({
                'error': 'Method Not Allowed',
                'message': f'The HTTP method {method} is not allowed for this endpoint.'
            }, status=405)
        

        if not task_id:
            return JsonResponse({'error': 'Task ID not provided'}, status=400)

    
        if method == 'GET':
            try:
                task = Task.objects.get(pk=task_id)
                return JsonResponse({
                    'task': {
                        'id': task.pk,
                        'title': task.title,
                        'description': task.description,
                        'status': task.status,
                        'owner': task.owner.pk
                    }
                })


            except Task.DoesNotExist:
                return JsonResponse({'error': 'Task not found'}, status=404)


        elif request.method == 'PUT':
            return handle_task_creation_or_update(request, 'Task successfully updated', 200, task_id)


        # DELETE METHOD.
        try:
            task = Task.objects.get(pk=task_id, owner=request.task_owner)
            task.delete()
            return JsonResponse({'message': 'Task deleted successfully'}, status=200)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        

    except Exception as e:
        # Handle any unexpected exceptions
        return JsonResponse({
            'error': 'Server Error',
            'message': str(e)  
        }, status=500)
