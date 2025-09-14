@echo off
echo Starting Newman Cyber Security Lab...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Initializing database...
echo.
echo Starting Flask application...
echo.
echo Open your browser and navigate to: http://localhost:5000
echo.
echo Test Accounts:
echo - Admin: admin / admin123
echo - User:  testuser / password
echo.
python app.py
pause
