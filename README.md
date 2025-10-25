# Live Flight Detector

A real-time flight tracking application that collects live flight data, stores it in Neo4j graph database, and provides comprehensive analysis and visualization.

## Features

- **Real-time Data Collection**: Streams live flight data from OpenSky Network API
- **Graph Database Storage**: Uses Neo4j to store flight relationships and routes
- **Data Analysis**: 5 simple and 5 complex Neo4j queries for insights
- **EDA (Exploratory Data Analysis)**: Statistical analysis and visualizations
- **Interactive Dashboard**: React frontend with real-time updates
- **Data Preprocessing**: Cleans and processes raw flight data

## Architecture

```
Frontend (React) ←→ Backend (Flask) ←→ Neo4j Database
                        ↓
                 OpenSky API (Live Data)
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- Neo4j Database
- OpenSky Network API access

## Quick Setup

### 1. Install Neo4j
```bash
# Using Docker
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest

# Or download from https://neo4j.com/download/
```

### 2. Backend Setup
```bash
cd live-flight-detector/backend
pip install -r requirements.txt
python app.py
```

### 3. Frontend Setup
```bash
cd live-flight-detector/frontend
npm install
npm start
```

## API Endpoints

### Data Collection
- `POST /api/start-collection` - Start continuous data collection
- `POST /api/stop-collection` - Stop data collection
- `POST /api/collect-once` - Collect data once
- `GET /api/flights` - Get current flight data
- `GET /api/statistics` - Get flight statistics

### Neo4j Queries
- `GET /api/queries/simple` - Execute 5 simple queries
- `GET /api/queries/complex` - Execute 5 complex queries

### Analysis
- `GET /api/eda` - Get EDA data and statistics

## Neo4j Queries

### Simple Queries
1. **Total Flights**: Count all flights in database
2. **Flights by Country**: Group flights by origin country
3. **Flights in Air**: Count flights currently airborne
4. **Average Altitude**: Calculate mean altitude of flights
5. **Unique Aircraft**: Count distinct aircraft identifiers

### Complex Queries
1. **Flight Routes**: Analyze departure-arrival patterns
2. **Busiest Airports**: Find airports with most traffic
3. **Altitude Distribution**: Categorize flights by altitude ranges
4. **Velocity Analysis**: Statistical analysis of flight speeds
5. **Country-Aircraft Analysis**: Aircraft types by country

## Data Flow

1. **Collection**: OpenSky API → Backend processing
2. **Storage**: Processed data → Neo4j graph database
3. **Analysis**: Neo4j queries → Statistical insights
4. **Visualization**: React frontend → Interactive dashboard

## Troubleshooting

### Common Issues

1. **Neo4j Connection Error**
   - Check if Neo4j is running on port 7687
   - Verify credentials in config.py

2. **API Rate Limits**
   - OpenSky API has rate limits
   - Adjust collection frequency if needed

3. **Frontend Not Loading**
   - Ensure backend is running on port 5000
   - Check browser console for errors

### Data Fetching Issues

If unable to fetch data:
1. Check Neo4j connection: `bolt://localhost:7687`
2. Verify OpenSky API access
3. Check backend logs for errors
4. Ensure all dependencies are installed

## Development

### Adding New Queries
Add new queries in `app.py` under the query endpoints.

### Custom Visualizations
Extend components in `frontend/src/components/` for new charts.

### Data Processing
Modify `flight_data_collector.py` for custom data processing logic.

## License

MIT License - Feel free to use and modify for your projects.
