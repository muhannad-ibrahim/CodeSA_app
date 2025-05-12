from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer
import os
import subprocess
from django.conf import settings
from django.http import FileResponse

class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Task operations."""
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = []  # Removed IsAuthenticated

    def perform_create(self, serializer):
        """Create a new task and process the PDF file using pdftk."""
        task = serializer.save()
        task.status = Task.TaskStatus.PROCESSING
        task.save()

        try:
            # Get input file path
            input_path = task.get_input_file_path()
            
            # Create output directory if it doesn't exist
            output_dir = os.path.join(settings.MEDIA_ROOT, 'output_files')
            os.makedirs(output_dir, exist_ok=True)
            
            # Set output file path
            output_filename = f"compressed_{task.id}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            # Compress PDF using pdftk
            # pdftk input.pdf output compressed.pdf compress
            subprocess.run([
                'pdftk',
                input_path,
                'output',
                output_path,
                'compress'
            ], check=True)

            # Update task with output file
            task.output_file = f'output_files/{output_filename}'
            task.status = Task.TaskStatus.COMPLETED
            task.save()

        except subprocess.CalledProcessError as e:
            task.status = Task.TaskStatus.FAILED
            task.error_message = f"PDF compression failed: {str(e)}"
            task.save()
        except Exception as e:
            task.status = Task.TaskStatus.FAILED
            task.error_message = str(e)
            task.save()

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download the processed PDF file."""
        task = self.get_object()
        
        if task.status != Task.TaskStatus.COMPLETED:
            return Response(
                {'error': 'Task is not completed yet'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not task.output_file:
            return Response(
                {'error': 'Output file not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            file_path = task.get_output_file_path()
            if not os.path.exists(file_path):
                return Response(
                    {'error': 'File not found on server'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get original filename without the 'compressed_' prefix
            original_filename = os.path.basename(task.input_file.name)
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{original_filename}"'
            return response
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 