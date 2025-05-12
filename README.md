# PDF Task Processor

A web application for processing PDF files with a Django REST Framework backend and React frontend.

## Project Structure

```
pdf-task-processor/
├── backend/                 # Django backend
│   ├── task_processor/     # Django project settings
│   ├── tasks/             # Django app for PDF processing
│   │   ├── models.py      # Task model definition
│   │   ├── serializers.py # API serializers
│   │   ├── views.py       # API views and PDF processing logic
│   │   └── urls.py        # URL routing
│   ├── media/             # Uploaded and processed files
│   └── requirements.txt   # Python dependencies
└── frontend/              # React frontend
    ├── public/           # Static files
    ├── src/             # React source code
    │   ├── components/  # React components
    │   ├── App.js      # Main App component
    │   └── index.js    # Entry point
    └── package.json    # Node.js dependencies
```

## Technologies Used

### Backend
- **Django**: Web framework
- **Django REST Framework**: API development
- **PDFtk**: PDF processing and compression
- **SQLite**: Database (can be changed to PostgreSQL for production)
- **CORS Headers**: Cross-origin resource sharing support

### Frontend
- **React**: UI library
- **Axios**: HTTP client
- **React Router**: Client-side routing
- **Bootstrap**: UI styling

## Features
- PDF file upload
- PDF compression using PDFtk
- Task status tracking
- Download processed PDFs
- Real-time status updates
- Responsive design

## Prerequisites

### Backend
- Python 3.8+
- PDFtk Server 2.02+
- Virtual environment (recommended)

### Frontend
- Node.js 14+
- npm or yarn

## Installation

### Backend Setup
1. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Install PDFtk:
   - Windows: Download and install from [PDFtk Server](https://www.pdflabs.com/tools/pdftk-server/)
   - Linux: `sudo apt-get install pdftk`
   - Mac: `brew install pdftk`

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

## API Endpoints

### Tasks
- `GET /api/tasks/`: List all tasks
- `POST /api/tasks/`: Create a new task
- `GET /api/tasks/{id}/`: Get task details
- `GET /api/tasks/{id}/download/`: Download processed PDF

## Development

### Backend Development
- The backend uses Django REST Framework for API development
- PDF processing is handled by PDFtk for efficient compression
- Task status is tracked in the database
- Media files are stored in the `media` directory

### Frontend Development
- React components are organized in the `components` directory
- Axios is used for API communication
- Bootstrap provides responsive styling
- Task status is updated in real-time

## Production Deployment
For production deployment:
1. Change `DEBUG = False` in settings.py
2. Use a production-grade database (PostgreSQL recommended)
3. Set up proper CORS settings
4. Configure proper media file storage
5. Use a production-grade web server (Nginx/Apache)
6. Set up proper security measures

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License. 