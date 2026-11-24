@echo off
echo ============================================
echo   AI Image Recognition Web Interface
echo ============================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if Flask is installed
echo.
echo Checking dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask not found. Installing dependencies...
    pip install -r requirements.txt
)

REM Start Flask application
echo.
echo Starting Flask server...
echo.
echo Access the web interface at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
