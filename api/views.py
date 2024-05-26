
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
from .models import Task, Token
from django.contrib.auth.models import User
import json
from typing import Dict


# Custom imports
from .validators import validate_user_inputs, validate_task_inputs
from .decorators import token_required
from .utils import handle_task_creation_or_update


@csrf_exempt
def register(request: HttpRequest) -> JsonResponse:
    """
        register view function.
        accepts only post method
    """

    if request.method != 'POST':
        return JsonResponse({
            'error': 'Invalid request method',
            'message': 'Only POST method is allowed for register view.'
        }, status=405)

    # check the return type of the validate_user_inputs function, if its a JSONRESPONSE object, that means an error was returned, simply return the error.
    if isinstance(validate_user_inputs(request), JsonResponse):
        return validate_user_inputs(request)

    # if no error unpack the result
    username, password = validate_user_inputs(request)
    
    # check if user already exists
    if not User.objects.filter(username=username).first(): 

        user = User(username=username)
        user.set_password(password)  #hash user password
        user.save()

        # create token for user
        token = Token.objects.create(user=user)

        return JsonResponse({
            'token': token.key,
            'expires_at': token.expires_at.now().strftime('%Y-%m-%d T%H:%M:%SZ')
        }, status=201)
    

    return JsonResponse({'Error:': 'user already exists, kindly login with user auth token'}, status=400)


# LOGIN USER FUNCTION
def login(request: HttpRequest) -> JsonResponse:
    pass

@csrf_exempt
def refresh_token(request: HttpRequest) -> JsonResponse:

    if request.method != 'POST':
        return JsonResponse({
            'error': 'Invalid request method',
            'message': 'Only POST method is allowed for token refresh.'
        }, status=405)
            
    
    # check the return type of the validate_user_inputs function, if its a JSONRESPONSE object, that means an error was returned, simply return the error.
    if isinstance(validate_user_inputs(request), JsonResponse):
        return validate_user_inputs(request)

    # if no error unpack the result
    username, password = validate_user_inputs(request)

    # authenticate user
    user = authenticate(username=username, password=password)

    # return json response if user is none
    if not user:
        return JsonResponse({
            'error': 'Invalid credentials',
            'message': 'Username or password is incorrect.'
        }, status=401)
    
      
    # try and get old token if token does not exist create new one.
    try:
        old_token = user.auth_token
        # revoke user previous token.
        old_token.revoke_token(delete=True)
    except Token.DoesNotExist:
        pass

    # create new token
    new_token = Token.objects.create(user=user)


    return JsonResponse({
            'token': new_token.key,
            'expires_at': new_token.expires_at.now().strftime('%Y-%m-%d T%H:%M:%SZ')
        }, status=201)


@csrf_exempt
@token_required
def task_manager(request: HttpRequest) -> JsonResponse:
    method = request.method

    if method not in ['GET', 'POST']:
        return JsonResponse({
            'error': 'Method Not Allowed',
            'message': f'The HTTP method {method} is not allowed for this endpoint.'
        }, status=405)

    try:
        if method == 'GET':
            all_tasks = Task.objects.all()
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
