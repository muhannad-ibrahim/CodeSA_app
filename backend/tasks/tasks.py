from celery import shared_task
from .models import Task
import os
from django.conf import settings
import subprocess

@shared_task
def process_pdf(task_id):
    """Celery task to process PDF files."""
    try:
        task = Task.objects.get(id=task_id)
        task.status = Task.TaskStatus.PROCESSING
        task.save()

        # Get input file path
        input_path = task.get_input_file_path()
        
        # Create output directory if it doesn't exist
        output_dir = os.path.join(settings.MEDIA_ROOT, 'output_files')
        os.makedirs(output_dir, exist_ok=True)
        
        # Set output file path
        output_filename = f"compressed_{task.id}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        # Compress PDF using pdftk
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