@echo off
setlocal

echo === Removing old virtual environment ===
IF EXIST venv (
    rmdir /s /q venv
)

echo === Creating new virtual environment ===
python -m venv venv

echo === Activating virtual environment ===
call venv\Scripts\activate.bat

echo === Installing dependencies ===
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

echo === Starting ngrok on port 8000 ===
start "" ngrok http 8000

timeout /t 2

echo === Launching FastAPI server ===
uvicorn app.main:app --reload

endlocal
