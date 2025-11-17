#!/bin/bash

# Start the development environment for the search app

echo "Starting Search App Development Environment..."

# Check if Python virtual environment exists
if [ ! -d "backend/env" ]; then
    echo "Creating Python virtual environment..."
    cd backend
    python3.9 -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt
    cd ..
else
    echo "Activating Python virtual environment..."
    cd backend
    source env/bin/activate
    pip3 install -r requirements.txt
    cd ..
fi

echo ""
echo "Starting Flask backend on port 5000..."
cd backend/
python src/app_controller.py  &
BACKEND_PID=$!
cd ../../

# echo "Starting React frontend on port 3000..."
# npm start &
# FRONTEND_PID=$!

echo ""
echo "🚀 Application started!"
echo "📱 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap 'echo "Stopping servers..."; kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait
