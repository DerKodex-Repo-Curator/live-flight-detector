# Troubleshooting Guide

## Common Issues and Solutions

### 1. Neo4j Connection Issues

**Problem**: Backend can't connect to Neo4j
```
Error: Failed to establish connection to Neo4j
```

**Solutions**:
- Check if Neo4j is running: `docker ps | grep neo4j`
- Verify connection string in `config.py`
- Test connection: `curl http://localhost:7474`
- Check Neo4j logs: `docker logs flight-neo4j`

### 2. Frontend Not Loading Data

**Problem**: Frontend shows "No flight data available"

**Solutions**:
- Check if backend is running on port 5000
- Verify API endpoints: `curl http://localhost:5000/api/flights`
- Check browser console for CORS errors
- Ensure backend is collecting data (click "Collect Once")

### 3. OpenSky API Issues

**Problem**: No flight data from API

**Solutions**:
- Check internet connection
- Verify API is accessible: `curl https://opensky-network.org/api/states/all`
- Check rate limits (API has usage limits)
- Try different time periods

### 4. Data Collection Not Working

**Problem**: Data collection starts but no data appears

**Solutions**:
- Check Neo4j connection first
- Verify data is being stored: Check Neo4j browser
- Check backend logs for errors
- Ensure OpenSky API is responding

### 5. Query Execution Errors

**Problem**: Neo4j queries return errors

**Solutions**:
- Check if data exists in database
- Verify query syntax
- Check Neo4j browser for data
- Run simple queries first

## Debugging Steps

### 1. Check Service Status
```bash
# Check if all services are running
docker ps
curl http://localhost:7474  # Neo4j
curl http://localhost:5000/api/flights  # Backend
curl http://localhost:3000  # Frontend
```

### 2. Check Logs
```bash
# Backend logs
cd backend && python app.py

# Neo4j logs
docker logs flight-neo4j

# Frontend logs (in browser console)
```

### 3. Test API Endpoints
```bash
# Test data collection
curl -X POST http://localhost:5000/api/collect-once

# Test statistics
curl http://localhost:5000/api/statistics

# Test queries
curl http://localhost:5000/api/queries/simple
```

### 4. Verify Data in Neo4j
1. Open Neo4j browser: http://localhost:7474
2. Login with neo4j/password
3. Run: `MATCH (n) RETURN count(n)`
4. Check for Flight nodes: `MATCH (f:Flight) RETURN f LIMIT 5`

## Performance Issues

### 1. Slow Data Collection
- Reduce collection frequency
- Check network connection
- Monitor API rate limits

### 2. Frontend Lag
- Reduce data refresh frequency
- Limit number of flights displayed
- Check browser performance

### 3. Neo4j Performance
- Add indexes for common queries
- Monitor database size
- Consider data retention policies

## Environment Setup Issues

### 1. Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Node.js Dependencies
```bash
cd frontend
npm install
```

### 3. Docker Issues
```bash
# Clean up containers
docker-compose down
docker system prune

# Rebuild
docker-compose up --build
```

## Data Issues

### 1. No Flight Data
- Check if OpenSky API is accessible
- Verify API key (if required)
- Check time zone settings
- Try different geographic regions

### 2. Incomplete Data
- Some flights may have missing fields
- Check data validation in collector
- Handle null values in queries

### 3. Data Quality
- Filter out invalid coordinates
- Handle altitude outliers
- Validate flight callsigns

## Quick Fixes

### Reset Everything
```bash
# Stop all services
docker-compose down
docker stop flight-neo4j
docker rm flight-neo4j

# Clean up
docker system prune

# Restart
./start.sh
```

### Manual Data Collection
```bash
# Start backend only
cd backend
python app.py

# In another terminal, test collection
curl -X POST http://localhost:5000/api/collect-once
```

### Check Data Flow
1. OpenSky API → Backend (check logs)
2. Backend → Neo4j (check connection)
3. Neo4j → Queries (check browser)
4. Backend → Frontend (check API)

## Still Having Issues?

1. Check all service logs
2. Verify network connectivity
3. Test each component individually
4. Check system resources (CPU, memory)
5. Consider firewall settings
6. Verify all ports are available

## Contact Support

If issues persist:
1. Collect all error logs
2. Note your system configuration
3. Describe the exact steps to reproduce
4. Include any error messages
