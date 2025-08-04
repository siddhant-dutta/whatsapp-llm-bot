@echo off
setlocal

echo === Deactivating any active virtual environment (manually if needed) ===
:: NOTE: 'deactivate' is a shell function, not a command — skip this in batch
:: If you're switching from another environment, close the terminal and re-run this script

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
pip install -r requirements.txt

echo === Starting ngrok on port 8000 ===
start "" ngrok http 8000

timeout /t 2

echo === Launching FastAPI server ===
uvicorn app.main:app --reload

endlocal
