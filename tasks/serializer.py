from .models import Task
from django.contrib.auth.models import User
from django.http import  HttpRequest
from django.utils import timezone
from typing import Any, Dict


class TaskSerializer:
    """
    A serializer for the Task model to facilitate the conversion 
    between Task instances and dictionary representations.
    This serializer provides methods to serialize Task objects 
    into a dictionary format suitable for JSON responses and to 
    deserialize dictionary data to create or update Task instances.
    """

    @staticmethod
    def to_dict(data: Task) -> Dict[str, Any]:
        """
        Serializes a Task instance into a dictionary representation.
        """

        # Ensure that the provided data is a Task instance
        if not isinstance(data, Task):
            raise ValueError("The provided data is not a valid Task instance.")
        
        # Constructing the dictionary representation of the Task
        to_json = {
            'id': data.pk, 
            'title': data.title, 
            'description': data.description, 
            'created_at': data.created_at,
            'status': data.status, 
            'owner': data.owner.pk 
        }

        return to_json
    
    @staticmethod
    def from_dict(request: HttpRequest, instance: Task = None, **kwargs: Dict) -> Task:
        """
        Deserializes a dictionary to create or update a Task instance.

        This method updates the Task instance if it is provided,
        otherwise, it creates a new Task instance using the provided
        keyword arguments.
        """        

        if instance:
            # Update the existing Task instance with new values
            instance.title = kwargs.get('title') 
            instance.description = kwargs.get('description')  
            instance.status = kwargs.get('status') 
            instance.owner = request.user

            # Save the updated instance to the database
            instance.save()

            return instance

        # Create a new Task instance using the provided keyword arguments
        return Task.objects.create(**kwargs)
