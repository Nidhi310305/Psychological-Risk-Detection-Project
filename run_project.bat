@echo off
echo Starting Backend Server...
start cmd /k "python -m uvicorn api_fastapi:app --reload"

echo Starting Frontend Server...
cd frontend
start cmd /k "npm run dev"

echo Both servers are starting! The frontend will usually be available at http://localhost:5173
echo The backend API will be running at http://localhost:8000
