# CodeAlpha Social Media Platform

A mini social media application built with Django, SQLite, HTML, CSS and JavaScript.

## Features
- User registration, login and logout
- User profile pages with bio and profile photo upload
- Create, edit and delete your own posts
- Text posts with optional image uploads
- Like / unlike posts
- Comment on posts and delete your own comments
- Follow / unfollow users
- Profile pages show posts, followers and following counts
- Search users
- Responsive layout

## Requirements
- Python 3.10+
- pip

## Run locally (Windows PowerShell)

```powershell
# 1. Open this project folder
cd CodeAlpha_SocialMediaPlatform

# 2. Create a virtual environment
py -m venv venv

# 3. Activate it
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
python -m pip install -r requirements.txt

# 5. Create database tables
python manage.py makemigrations accounts posts
python manage.py migrate

# 6. Start the development server
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Create an admin account (optional)
```powershell
python manage.py createsuperuser
```
Then visit http://127.0.0.1:8000/admin/.

## Project structure
- `socialhub/` - Django project configuration
- `accounts/` - profile, follow and user search features
- `posts/` - posts, likes and comments
- `templates/` - HTML templates
- `static/` - CSS and JavaScript
- `media/` - uploaded post/profile images (created automatically)

## Notes
- This is a learning/demo project. Before public production deployment, configure a strong `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, HTTPS, secure cookies, backups and a production database/storage service.
- The default database is SQLite and is created by `migrate`.
