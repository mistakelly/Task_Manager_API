from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate

from django.utils.timezone import now

# excempt csrf token
from django.views.decorators.csrf import csrf_exempt


# database
from .models import Task, Token
from django.contrib.auth.models import User
import json
from typing import Dict


# custom imports
from .validators import token_required

@csrf_exempt
def register(request: HttpRequest) -> JsonResponse:
    """
        register view function.
        accepts only post method
    """

    try:
        if request.method != 'POST':
            return JsonResponse({
                'error': 'Invalid request method',
                'message': 'Only POST method is allowed for register view.'
            }, status=405)

        data = json.loads(request.body.decode('utf-8'))

        username = data.get('username')
        password = data.get('password')

        if not username:
            return JsonResponse({'error': 'username cannot be null'}, status=400)

        if not password:
            return JsonResponse({'error': 'password cannot be null'}, status=400)
        
        if not User.objects.filter(username=username).first(): # check if user already exists

            user = User(username=username)
            user.set_password(password)  #hash user password
            user.save()


            token = Token.objects.create(user=user) # create token for user

            return JsonResponse({
                'token': token.key,
                'expires_at': token.expires_at.now().strftime('%Y-%m-%d T%H:%M:%SZ')
            }, status=201)
        else:
            return JsonResponse({'Error:': 'user already exists, kindly login with user auth token'})
        
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid json format'}, status=400)

