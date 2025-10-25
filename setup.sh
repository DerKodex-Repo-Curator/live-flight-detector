#!/bin/bash

echo "🚀 Setting up Live Flight Detector..."

# Check if Neo4j is running
echo "📊 Checking Neo4j connection..."
if ! curl -s http://localhost:7474 > /dev/null; then
    echo "❌ Neo4j is not running. Please start Neo4j first:"
    echo "   docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest"
    echo "   Or download from https://neo4j.com/download/"
    exit 1
fi

echo "✅ Neo4j is running"

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd ../frontend
npm install

echo "✅ Setup complete!"
echo ""
echo "🎯 To start the application:"
echo "1. Backend: cd backend && python app.py"
echo "2. Frontend: cd frontend && npm start"
echo ""
echo "🌐 Access the application at http://localhost:3000"
echo "📊 Neo4j browser at http://localhost:7474"
