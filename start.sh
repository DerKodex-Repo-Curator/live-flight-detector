#!/bin/bash

echo "🛩️ Starting Live Flight Detector..."

# Check if Neo4j is running
if ! curl -s http://localhost:7474 > /dev/null 2>&1; then
    echo "🚀 Starting Neo4j with Docker..."
    docker run -d --name flight-neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
    echo "⏳ Waiting for Neo4j to start..."
    sleep 10
fi

echo "✅ Neo4j is running at http://localhost:7474"

# Start backend
echo "🚀 Starting backend..."
cd backend
python app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
echo "🚀 Starting frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "✅ Application started!"
echo "🌐 Frontend: http://localhost:3000"
echo "📊 Neo4j Browser: http://localhost:7474"
echo "🔧 Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
wait
