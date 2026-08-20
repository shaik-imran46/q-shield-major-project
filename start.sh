#!/bin/bash
set -e

echo "================================================================================"
echo "  Q-SHIELD: Adaptive Multi-Agent Cyber-Risk & Post-Quantum Security Framework"
echo "================================================================================"

echo "[1/3] Setting up Python virtual environment..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi
pip install -r requirements.txt

echo "[2/3] Starting FastAPI Backend on http://localhost:8000..."
python3 run_server.py &
BACKEND_PID=$!
cd ..

echo "[3/3] Setting up Next.js Frontend..."
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!

echo "================================================================================"
echo "  Q-Shield SOC Dashboard is now running!"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API & Docs: http://localhost:8000/docs"
echo "================================================================================"

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
