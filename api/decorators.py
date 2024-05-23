from django.http import JsonResponse
from .models import Token

from functools import wraps

# TOKEN REQUIRED FUNCTION
def token_required(func):
    """
    Decorator to ensure a valid token is provided in the Authorization header 
    of the request.

    This decorator checks whether the token is:
        - Present
        - Correctly formatted
        - Active
        - Not expired

    If the token is valid, it allows access to the wrapped view function. 
    If not, it returns a JsonResponse indicating the error with an appropriate 
    status code.

    Args:
        func (callable): The view function to be wrapped and protected by this decorator.

    Returns:
        callable: The wrapped view function if the token is valid; otherwise, a 
        JsonResponse indicating the error.

    Notes:
        - Ensure that the Authorization header starts with "Token ".
        - If the token is revoked or expired, a 401 Unauthorized response is returned.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        auth_header = request.headers.get('Authorization')


        if auth_header is None:
            return JsonResponse({
                'error': 'Authorization header missing',
                'message': 'The Authorization header is required to access this resource.'
            }, status=401)

        if not auth_header.startswith('Token '):
            return JsonResponse({
                'error': 'Invalid Authorization header format',
                'message': 'Ensure the Authorization header starts with "Token" followed by a space and your token.'
            }, status=401)

        token_key = auth_header.split()[1]

        try:
            token: Token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return JsonResponse({
                'error': 'Invalid token',
                'message': 'The provided token does not exist or is invalid.'
            }, status=401)
        
        # get the owner of the token and attach it to request object.
        request.task_owner = token.user
        
        # Check if the token is active and not expired
        if token.is_active and not token.is_expired:
            return func(*args, **kwargs)  # Call the wrapped function

        # Token is either revoked or expired
        return JsonResponse({
            'error': 'Token revoked or expired',
            'message': 'The provided token is revoked or may have expired. Please obtain a new token.'
        }, status=401)

       

    # return wrapper function
    return wrapper