@echo off
echo Activating virtual environment...
call venv\Scripts\activate

:: Start ngrok tunnel in a new window
start "" ngrok http 8000

:: Optional wait for ngrok to fully start
timeout /t 2

:: Start FastAPI app
uvicorn app.main:app --reload
