
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
from .models import Token
from django.contrib.auth.models import User
import json
from typing import Dict


# Custom imports
from .validators import validate_user_inputs



# Create your views here.
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


    validated_data = validate_user_inputs(request)

    # check the return type of the validate_user_inputs function, if its a JSONRESPONSE object, that means an error was returned, simply return the error.
    if isinstance(validated_data, JsonResponse):
        return validated_data

    # if no error unpack the result
    username, password = validated_data
    
    # check if user already exists
    if not User.objects.filter(username=username).first(): 

        user = User(username=username)
        user.set_password(password)  #hash user password
        user.save()

        # create token for user
        token = Token.objects.create(user=user)

        return JsonResponse({
            'id': user.pk,
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


def get_users(request: HttpRequest) -> JsonResponse:
    pass



def get_user(request: HttpRequest) -> JsonResponse:
    pass