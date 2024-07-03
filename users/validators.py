import json
from django.http import JsonResponse

# VALIDATE USER INPUTS FUNCTION
def validate_user_inputs(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid Json Format'}, status=400)

     # Using Python's walrus operator (:=) to check and assign values in a single expression
    if not (username := data.get('username')):
        return JsonResponse({'error': 'username cannot be null'}, status=400)

    if not (password := data.get('password')):
        return JsonResponse({'error': 'password cannot be null'}, status=400)
    

    
    return username, password