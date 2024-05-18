from django.http import JsonResponse
from .models import Token

# TOKEN REQUIRED FUNCTION
def token_required(func):
    """
    Decorator that ensures a valid token is provided in the Authorization header 
    of the request. It checks whether the token is present, correctly formatted, 
    active, and not expired before allowing access to the wrapped view function.

    Args:
        func (callable): The view function to be wrapped and protected by this decorator.

    Returns:
        callable: The wrapped view function if the token is valid; otherwise, a 
        JsonResponse indicating the error with an appropriate status code.

    Raises:
        JsonResponse: Returns a 401 Unauthorized response if:
            - The Authorization header is missing.
            - The Authorization header does not start with "Token ".
            - The provided token does not exist in the database.
            - The token is revoked or expired.

    Example:
        @token_required
        def my_view(request):
            # view logic here
    """


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