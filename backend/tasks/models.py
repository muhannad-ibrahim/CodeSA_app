from django.db import models
from django.core.validators import FileExtensionValidator
import os
import uuid

class Task(models.Model):
    """Model representing a PDF processing task."""
    
    class TaskStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    input_file = models.FileField(
        upload_to='input_files/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    output_file = models.FileField(upload_to='output_files/', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task {self.id} - {self.status}"

    def get_input_file_path(self):
        """Get the absolute path of the input file."""
        return self.input_file.path

    def get_output_file_path(self):
        """Get the absolute path of the output file."""
        if self.output_file:
            return self.output_file.path
        return None

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ] 