import json

# DJANGO IMPORTS
from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import HttpRequest

# TYPE ANNOTATION
from typing import Dict, Tuple, List

import json
from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import HttpRequest
from typing import Dict, Tuple, List

def error_response(message: str, status_code=400) -> JsonResponse:
    """
    Error Response Helper:
    Generates a JsonResponse with a custom error message and status code.
    """
    return JsonResponse({'error': message}, status=status_code)

def validate_inputs(data: Dict, inputs: List) -> Dict:
    """
    Validate Inputs:
    Checks if the required inputs are present in the provided data.
    If any required input is missing, returns an error response.
    """
    for task_input in inputs:
        if not data.get(task_input):  # Check if the input is missing or empty
            return error_response(f'{task_input.capitalize()} cannot be null or empty.')
    return data

def validate_user_inputs(request: HttpRequest) -> Dict:
    """
    Validate User Inputs:
    Extracts and validates the 'username' and 'password' fields from the request body.
    """
    try:
        # Parse JSON request body
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return error_response('Invalid JSON format')

    # Validate presence of required inputs: 'username' and 'password'
    validated_data = validate_inputs(data, ['username', 'password'])

    # If validation failed, return the error response
    if isinstance(validated_data, JsonResponse):
        return validated_data

    # Extract 'username' and 'password' from validated data
    username = validated_data.get('username')
    password = validated_data.get('password')

    return username, password

def validate_task_inputs(request: HttpRequest) -> Tuple:
    """
    Validate Task Inputs:
    Validates task-related fields such as 'title', 'description', 'owner', and 'status'.
    It also validates 'created_at' and ensures it includes both date and time information.
    """
    # List of valid task statuses
    TASK_STATUS = ['pending', 'in-progress', 'completed', 'cancelled', 'on-hold']

    try:
        # Parse JSON request body
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return error_response('Invalid JSON format')

    # Validate presence of required task inputs: 'title', 'description', 'owner', 'status'
    validated_data = validate_inputs(data, ['title', 'description', 'owner', 'status'])
    
    # If validation failed, return the error response
    if isinstance(validated_data, JsonResponse):
        return validated_data

    # Extract task fields from validated data
    title = data.get('title')
    description = data.get('description')
    owner_id = data.get('owner')
    status = data.get('status')

    # Check if the provided status is valid
    if status not in TASK_STATUS:
        return error_response(
            'Invalid task status. Must be one of: pending, in-progress, completed, cancelled, or on-hold.'
        )

    # Handle the 'created_at' field: If not provided, use the current timestamp; otherwise, validate the provided date
    created_at = data.get('created_at')
    if not created_at:
        # Use the current time if 'created_at' is missing
        created_at = timezone.now()
    else:
        # Parse 'created_at' into a datetime object
        created_at = parse_datetime(created_at)
        if created_at is None:
            # Return an error if the date format is invalid
            return error_response("Invalid date format. Please provide 'YYYY-MM-DDTHH:MM:SSZ'.")

        # If only date is provided (e.g., '2024-10-12'), set a default time (e.g., 12:00 PM)
        if created_at.hour == 0 and created_at.minute == 0 and created_at.second == 0:
            created_at = created_at.replace(hour=12)  # Default time if not provided

        # Ensure the 'created_at' datetime is timezone-aware, if it's not already
        if created_at.tzinfo is None:
            created_at = timezone.make_aware(created_at)
    

    return {
        'title': title,
        'description': description,
        'status': status,
        'owner_id': owner_id,
        'created_at': created_at,
    }