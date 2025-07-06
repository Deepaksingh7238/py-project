# Job Portal API

A Django REST API for managing companies, job posts, and applicants.

## Setup

1. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run migrations and start the server:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```
