# HelpLink - Community Help Platform

A Django-based web application that connects people who need help with those willing to offer assistance.

## Features

- User registration and authentication
- Help request posting and management
- Help offer system with notifications
- User profiles with reputation system
- Category-based help requests

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up PostgreSQL database and update settings
6. Run migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Run the development server: `python manage.py runserver`

## Deployment on Render

### Prerequisites

1. Create a Render account at https://render.com
2. Create a PostgreSQL database on Render
3. Fork or clone this repository to your GitHub

### Environment Variables

Set the following environment variables in your Render dashboard:

```
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### Deployment Steps

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Configure the service:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn HelpLink.wsgi:application --bind 0.0.0.0:$PORT`
4. Add environment variables as listed above
5. Deploy the service

### Database Setup

After deployment, run the following commands in Render's shell or via a one-off job:

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Technologies Used

- Django 5.2.8
- PostgreSQL
- Tailwind CSS
- Gunicorn (production)
- WhiteNoise (static files)

## License

This project is licensed under the MIT License.