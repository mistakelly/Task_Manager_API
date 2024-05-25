from django.http import JsonResponse, HttpRequest


# custom imports
from .models import Task
from .validators import validate_task_inputs


def handle_task_creation_or_update(request: HttpRequest, message: str, status_code, task_id=None) -> JsonResponse:
    method = request.method
    if isinstance(validate_task_inputs(request), JsonResponse):
            return validate_task_inputs(request)

    title, desc, status, owner_id = validate_task_inputs(request)

    # Get the task owner from the request object
    owner = request.task_owner

    if owner.pk != owner_id:
        return JsonResponse({
            'error': 'Invalid Token',
            'message': 'The provided token is invalid or has expired.'
        }, status=401)

    # Save task to the database
    if method == 'POST':
        task = Task.objects.create(title=title, description=desc, status=status, owner=owner)
    elif method == 'PUT':
        try:
            task = Task.objects.get(pk=task_id)
            task.title = title
            task.description = desc
            task.status = status
            task.save()
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
       

    return JsonResponse(
            {
                'message': f'{message}',
                'task': {
                    'id': task.pk,
                    'title': title,
                    'description': desc,
                    'status': status,
                    'owner': owner.pk
                }
            }, status=status_code)
         