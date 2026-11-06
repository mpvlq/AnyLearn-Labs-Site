@echo off
echo Starting AnyLearn Labs development server...
call venv\Scripts\activate
python manage.py runserver
