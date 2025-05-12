from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""
    
    class Meta:
        model = Task
        fields = [
            'id',
            'description',
            'input_file',
            'output_file',
            'status',
            'error_message',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'output_file',
            'status',
            'error_message',
            'created_at',
            'updated_at'
        ]

    def validate_input_file(self, value):
        """Validate that the uploaded file is a PDF."""
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return value 