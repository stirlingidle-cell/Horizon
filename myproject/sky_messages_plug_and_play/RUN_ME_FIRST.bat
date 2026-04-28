@echo off
echo ================================
echo SKY Messages Django Project
echo ================================
echo.
echo Installing Django if needed...
python -m pip install -r requirements.txt
echo.
echo Making migrations...
python manage.py makemigrations
echo.
echo Applying database migrations...
python manage.py migrate
echo.
echo Creating demo users...
python create_demo_users.py
echo.
echo Starting server...
echo Open this in Chrome: http://127.0.0.1:8080/
python manage.py runserver
pause
