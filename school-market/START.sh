#!/bin/bash
echo "========================================"
echo "  Maktab Market — Ishga tushirish"
echo "========================================"

# Backend
echo "[1/2] Backend ishga tushmoqda..."
cd server && npm start &
BACKEND_PID=$!

# Wait a bit
sleep 2

# Frontend
echo "[2/2] Frontend ishga tushmoqda..."
cd ..
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "  Sayt: http://localhost:5173"
echo "  API:  http://localhost:5000/api"
echo "========================================"

wait
